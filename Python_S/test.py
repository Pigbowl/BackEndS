# 在Python解释器中
from read_part_catalogue import create_part_catalogue
from read_chipset_catalogue import create_chipset_catalogue

result = create_chipset_catalogue('../DataStorage/database.xlsx')
print(result)

# 如果需要处理JSON数据
import json
data = json.loads(result)
print(data)