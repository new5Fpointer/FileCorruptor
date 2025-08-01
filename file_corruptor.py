# file_corruptor.py
# file_corruptor.py
import os
import random
import re

class FileCorruptor:
    """增强版文件损坏处理器"""
    def __init__(self, protect_head=1024, protect_tail=1024):
        self.protect_head = protect_head
        self.protect_tail = protect_tail
    
    def corrupt_fixed_interval(self, input_path, output_path, interval, 
                              protect_head=None, protect_tail=None,
                              replace_value="random"):
        """
        固定间隔损坏模式
        
        参数:
            replace_value: 可以是:
                "random" - 随机字节值 (默认)
                "0xXX" - 十六进制值 (如 "0xFF")
                "XX" - 十进制值 (如 "255")
                byte - 字节值 (如 b'\x55')
        """
        protect_head = protect_head if protect_head is not None else self.protect_head
        protect_tail = protect_tail if protect_tail is not None else self.protect_tail
        
        # 解析替换值
        replace_byte = self._parse_replace_value(replace_value)
        
        file_size = os.path.getsize(input_path)
        corrupt_end = max(0, file_size - protect_tail)
        
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            position = 0
            for chunk in self._read_in_chunks(fin):
                chunk_arr = bytearray(chunk)
                for i in range(len(chunk_arr)):
                    global_pos = position + i
                    if global_pos < protect_head or global_pos >= corrupt_end:
                        continue
                    if global_pos % interval == 0:
                        chunk_arr[i] = replace_byte if isinstance(replace_byte, int) else random.randint(0, 255)
                fout.write(chunk_arr)
                position += len(chunk_arr)

    def corrupt_random_rate(self, input_path, output_path, rate,
                           protect_head=None, protect_tail=None,
                           replace_value="random"):
        """
        随机比例损坏模式
        
        参数:
            replace_value: 可以是:
                "random" - 随机字节值 (默认)
                "0xXX" - 十六进制值 (如 "0xFF")
                "XX" - 十进制值 (如 "255")
                byte - 字节值 (如 b'\x55')
        """
        protect_head = protect_head if protect_head is not None else self.protect_head
        protect_tail = protect_tail if protect_tail is not None else self.protect_tail
        
        # 解析替换值
        replace_byte = self._parse_replace_value(replace_value)
        
        file_size = os.path.getsize(input_path)
        corruptable_size = max(0, file_size - protect_head - protect_tail)
        num_to_corrupt = int(corruptable_size * rate)
        
        # 生成随机损坏位置
        corrupt_positions = set()
        if corruptable_size > 0:
            corrupt_positions = set(random.sample(
                range(protect_head, file_size - protect_tail),
                min(num_to_corrupt, corruptable_size)
            ))
        
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            position = 0
            for chunk in self._read_in_chunks(fin):
                chunk_arr = bytearray(chunk)
                for i in range(len(chunk_arr)):
                    if (position + i) in corrupt_positions:
                        chunk_arr[i] = replace_byte if isinstance(replace_byte, int) else random.randint(0, 255)
                fout.write(chunk_arr)
                position += len(chunk_arr)
    
    def replace_specific_bytes(self, input_path, output_path, replace_value,
                              protect_head=None, protect_tail=None):
        """
        替换所有字节为特定值
        
        参数:
            replace_value: 可以是:
                "random" - 随机字节值 (默认)
                "0xXX" - 十六进制值 (如 "0xFF")
                "XX" - 十进制值 (如 "255")
                byte - 字节值 (如 b'\x55')
        """
        protect_head = protect_head if protect_head is not None else self.protect_head
        protect_tail = protect_tail if protect_tail is not None else self.protect_tail
        
        # 解析替换值
        replace_byte = self._parse_replace_value(replace_value)
        
        file_size = os.path.getsize(input_path)
        corrupt_end = max(0, file_size - protect_tail)
        
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            position = 0
            for chunk in self._read_in_chunks(fin):
                chunk_arr = bytearray(chunk)
                for i in range(len(chunk_arr)):
                    global_pos = position + i
                    if global_pos < protect_head or global_pos >= corrupt_end:
                        continue
                    chunk_arr[i] = replace_byte if isinstance(replace_byte, int) else random.randint(0, 255)
                fout.write(chunk_arr)
                position += len(chunk_arr)
    
    def _parse_replace_value(self, value):
        """解析替换值"""
        if value == "random":
            return None  # 表示使用随机值
        
        if isinstance(value, bytes) and len(value) == 1:
            return value[0]  # 字节值
        
        if isinstance(value, int):
            return max(0, min(255, value))  # 确保在0-255范围内
        
        if isinstance(value, str):
            # 尝试解析十六进制格式 (0xXX)
            hex_match = re.match(r"0x([0-9a-fA-F]{1,2})$", value)
            if hex_match:
                return int(hex_match.group(1), 16)
            
            # 尝试解析十进制格式
            try:
                dec_value = int(value)
                return max(0, min(255, dec_value))
            except ValueError:
                pass
        
        # 默认返回随机值
        return None

    def _read_in_chunks(self, file_object, chunk_size=8*1024*1024):
        """文件分块读取生成器"""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data