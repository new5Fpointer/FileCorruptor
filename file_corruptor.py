# file_corruptor.py
import os
import random

class FileCorruptor:
    """文件损坏处理器"""
    def __init__(self, protect_head=1024, protect_tail=1024):
        self.protect_head = protect_head
        self.protect_tail = protect_tail

    def corrupt_fixed_interval(self, input_path, output_path, interval, 
                              protect_head=None, protect_tail=None):
        """固定间隔损坏模式"""
        protect_head = protect_head if protect_head is not None else self.protect_head
        protect_tail = protect_tail if protect_tail is not None else self.protect_tail
        
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
                        chunk_arr[i] = random.randint(0, 255)
                fout.write(chunk_arr)
                position += len(chunk_arr)

    def corrupt_random_rate(self, input_path, output_path, rate,
                           protect_head=None, protect_tail=None):
        """随机比例损坏模式"""
        protect_head = protect_head if protect_head is not None else self.protect_head
        protect_tail = protect_tail if protect_tail is not None else self.protect_tail
        
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
                        chunk_arr[i] = random.randint(0, 255)
                fout.write(chunk_arr)
                position += len(chunk_arr)

    def _read_in_chunks(self, file_object, chunk_size=8*1024*1024):
        """文件分块读取生成器"""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data