import os
import sys
from openai import OpenAI

debug = os.environ.get('DEBUG', False)

prompts_file = sys.argv[1] if len(sys.argv) > 1 else 'prompts.txt'
output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'

with open(prompts_file, 'r') as f:
  prompts = f.readlines()

# get the openai model name from the env var if set, default to gpt-3.5-turbo
openai_api_model = os.environ.get('OPENAI_API_MODEL', 'gpt-3.5-turbo')
print(f'using openai model: {openai_api_model}')

# get the openai api key from the env var if set, default to empty string
openai_api_key = os.environ.get('OPENAI_API_KEY', '')
if debug == True:
  print(f'openai api key: {openai_api_key}')

if openai_api_key == '':
  print('no openai api key set, exiting')
  exit(1)

client = OpenAI(
  api_key = openai_api_key
)


iters = 10
f = open(output_file, 'w')

for this_prompt in prompts:
  user_prompt = f"Generate a list of {iters} sentences with approximately the same meaning as \"{this_prompt}\""
  print(f'original prompt: {this_prompt}')

  response = client.chat.completions.create(
    model = openai_api_model,
    temperature = 1.6,
    messages = [
      {
        "role": "system",
        "content": "you are a paraphrasing bot designed to provide a rewording of phrases that are grammatically different but semantically similar. you should reword things creatively, but in a manner that approximates the same intent as the original message. your response should be returned in a JSONL array of strings."
      },
      {
        "role": "user",
        "content": user_prompt
      }
    ]
  )

  gen_response = response.choices[0].message.content
  f.write(gen_response)
  print(gen_response)

f.close()

# prompt="This is a test",
# max_tokens=5,
# temperature=1,
# top_p=1,
# frequency_penalty=0,
# presence_penalty=0,
# stop=["\n"]
