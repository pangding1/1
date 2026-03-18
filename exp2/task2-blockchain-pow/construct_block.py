import hashlib
import time

# 区块类
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # 金融场景下：交易信息
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # 理解：所有字段参与哈希，确保任何修改都会改变 hash
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# 【任务】区块链类核心逻辑
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # 难度系数，控制前缀 0 的个数

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    # 任务 1：实现挖矿逻辑 (PoW)
    def mine_block(self, new_block) -> None:
        # PoW核心：找到一个nonce值，让区块哈希以指定数量的0开头
        target = "0" * self.difficulty  # 难度目标：前缀有2个0
        while new_block.hash[:self.difficulty] != target:
            new_block.nonce += 1  # 随机数递增，暴力破解
            new_block.hash = new_block.calculate_hash()  # 重新计算哈希
        
        # 挖矿成功，将区块加入链
        self.chain.append(new_block)
        print(f"Block Mined! Hash: {new_block.hash}")

    # 任务 2：实现链的完整性验证
    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # 检查点 1：当前区块的哈希值是否重新计算后一致（防篡改）
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # 检查点 2：当前区块的 previous_hash 是否指向上一个区块的真实哈希（防链断裂）
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # 额外检查：验证PoW是否有效（可选，增强安全性）
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

if __name__ == "__main__":
    my_coin = Blockchain()
    # 添加第一笔交易并挖矿
    new_tx = Block(1, time.time(), "A pays B $100", my_coin.get_latest_block().hash)
    my_coin.mine_block(new_tx)
    
    # 验证链的完整性（初始状态）
    print(f"Chain Valid? {my_coin.is_chain_valid()}")  # 输出 True
    
    # 尝试篡改区块数据
    my_coin.chain[1].data = "A pays B $1000000" 
    # 再次验证（篡改后应该失效）
    print(f"Chain Valid after tampering? {my_coin.is_chain_valid()}")  # 输出 False
