async def calculate_cost(token_usage, model_name):
    prompt_tokens = token_usage['prompt_tokens']  # system prompt + user query + data from rag
    completion_tokens = token_usage['completion_tokens']  # llm answer - output
    total_tokens = token_usage['total_tokens']

    print(f'Prompt tokens: {prompt_tokens}')
    print(f'Completion tokens: {completion_tokens}')
    print(f'Total tokens: {total_tokens}')
    # Cost for deepseek-chat
    if model_name=="deepseek-chat":
        input_cost = prompt_tokens / 1_000_000 * 0.14
        output_cost = completion_tokens / 1_000_000 * 0.28
        total_cost = input_cost + output_cost
    # Cost for deepseek-reasoner
    else:
        input_cost = prompt_tokens / 1_000_000 * 0.55
        output_cost = completion_tokens / 1_000_000 * 2.19
        total_cost = input_cost + output_cost

    print(f'Input cost: ${input_cost:.6f}')
    print(f'Output cost: ${output_cost:.6f}')
    print(f'\nTOTAL COST: ${total_cost:.6f}\n')

