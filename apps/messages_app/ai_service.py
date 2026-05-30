import json
import urllib.request
import urllib.error


def chat_with_ai(ai_config, user_message, conversation_history=None):
    """
    Call an OpenAI-compatible API to get AI response.

    Args:
        ai_config: AIConfig model instance
        user_message: The user's message string
        conversation_history: Optional list of previous messages for context

    Returns:
        dict with 'success' bool and either 'content' or 'error'
    """
    if not ai_config.is_configured():
        return {'success': False, 'error': 'AI未配置，请先在私信设置中配置AI参数'}

    messages = []

    if ai_config.system_prompt:
        messages.append({'role': 'system', 'content': ai_config.system_prompt})

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({'role': 'user', 'content': user_message})

    api_url = ai_config.api_base_url.rstrip('/') + '/chat/completions'

    payload = {
        'model': ai_config.model_name,
        'messages': messages,
        'temperature': ai_config.temperature,
        'max_tokens': ai_config.max_tokens,
    }

    data = json.dumps(payload).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ai_config.api_key}',
    }

    req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            return {'success': True, 'content': content.strip()}
    except urllib.error.HTTPError as e:
        error_body = ''
        try:
            error_body = e.read().decode('utf-8')
        except Exception:
            pass
        return {'success': False, 'error': f'API请求失败({e.code}): {error_body[:200]}'}
    except urllib.error.URLError as e:
        return {'success': False, 'error': f'网络连接失败: {str(e.reason)}'}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {'success': False, 'error': f'API响应格式错误: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'AI请求异常: {str(e)}'}
