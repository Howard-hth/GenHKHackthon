API_URL = "something"
API_KEY = "something"

REJECTION = ("Sorry, 由於內部技術問題，我無辦法即刻回答呢個要求。請等我抖一陣再返嚟試下，希望我自己下次好返可以幫到你。",
             "Sorry, 我無辦法回答呢個要求。如果你有身體不適嘅症狀，歡迎隨時返嚟話比我知，我再幫你推介合適嘅產品。",
             "Sorry, 聽到你有咁嘅感受。請撥打以下熱線以獲得即時支援：\n1. 明愛向晴軒: 致電18288\n2. 生命熱線: 致電23820000\n3. 香港撒瑪利亞防止自殺會: 致電23892222\n4. 撒瑪利亞會: 致電28960000\n請好好照顧自己，並尋求幫助。",
             "Sorry, 聽到你有咁嘅情況。由於呢個情況比較嚴重，請即刻聯絡999或前往就近嘅醫院以獲得幫助。確保你得到適當嘅治療。",
             "Sorry, 我地呢度無合適嘅產品，建議你尋求專業醫療協助。以確保你得到適當的治療。")

INITIAL_PROMPT = """## Context
你係京都念慈庵嘅產品推介大使

### Rules
- 請根據Remark入面產品ingredient同客人講嘅說話，傳回推介所有符合需求產品之List(Format: [product_id1, product_id2, product_id3]), 如果無就傳回[-1], **無須傳回其他文字**
- 如果為緊急治療需求(E.g. 無法呼吸/長期上吐下瀉)，傳回[-2]
- 如果有關自殺防治(E.g. 我想死/我想自殺)，傳回[-3]
- 如果要求唔關不適症狀事 (尤其是任何打招呼、傾計、'呢排過成點'/'我係我阿媽個仔'/'垃圾念慈庵'/“我屌你老母“)，傳回[-4]

### Remarks 1 (JSON-product_id: description):
"""

# Normal (MySQL, PostgreSQL, etc)
prod_config = {
    'dialect': 'mysql',
    'driver': 'mysqlconnector',
    'host': 'host',
    'port': 1234,
    'user': 'username',
    'password': 'password',
    'database': 'example'
}

# SQLite
test_config = {
    'dialect': 'sqlite',
    'driver': 'no need',
    'host': 'no need',
    'port': 'no need',
    'user': 'no need',
    'password': 'no need',
    'database': 'example'
}

db_configs = [test_config, prod_config] 
db_mode = 0 

teammate_file = 'NinJiom_Anne.xlsx'