import asyncio, os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))
from experiments.tier2_council.runner import CostCalculator, get_client, DB_PATH

async def test():
    cost_calc = CostCalculator(DB_PATH)
    client = get_client('gpt-6.1-sol', cost_calc)
    print(f'Client endpoint: {client.endpoint}')
    print(f'Client masked key: {client.api_key[:8]}...{client.api_key[-4:]}')
    prompt = 'Phân tích tin nhắn SMS sau và xác định [SCAM] hay [HAM]:\nTin nhắn: "VCB tran trong thong bao tai khoan cua ban bi khoa, truy cap https://vcb-security.com de mo khoa."'
    res = await client.execute(prompt)
    print('Predicted Label:', res.predicted_label)
    print('Confidence:', res.confidence)
    print('Duration:', res.duration_ms, 'ms')
    print('Cost:', res.cost_usd)
    print('Raw Output excerpt:', res.raw_output[:120])

if __name__ == '__main__':
    asyncio.run(test())
