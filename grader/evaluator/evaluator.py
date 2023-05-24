import openai
import os

openai.api_key = "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"

def completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def evaluate(prompt):
    if len(prompt) > 20000:
        print('too long prompt', len(prompt))
        return None

    print('got prompt\n', prompt)
    res = completion(prompt)
    print('got ai response\n', res)

    return res
