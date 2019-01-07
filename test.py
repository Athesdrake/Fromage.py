import fromage

if __name__ == '__main__':
	import json

	with open('test.config') as f:
		config = json.load(f)

	async def test():
		client = fromage.Client()
		await client.connect(config['username'], config['password'], True)
		u:fromage.User = await fromage.User.get('Athesdrake#0000')
		print(u)
		print(u.profile)
		await client.close()

	import asyncio

	loop = asyncio.get_event_loop()
	loop.run_until_complete(test())

# TODO: compile regex
# TODO: add events