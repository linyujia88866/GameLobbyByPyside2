import requests


# 调用GET接口
def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data: {response.status_code}")


# 调用POST接口
def post_request(url, data):
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to post data: {response.status_code}")


def query_note(title):
    get_url = f'http://127.0.0.1:8888/note_content/{title}'
    # 发起请求
    get_response = get_request(get_url)
    return get_response


def query_notes():
    # 示例URL
    get_url = f'http://127.0.0.1:8888/all_notes'
    # 发起请求
    get_response = get_request(get_url)
    return get_response


def query_cates():
    # 示例URL
    get_url = f'http://127.0.0.1:8888/all_cate'
    # 发起请求
    get_response = get_request(get_url)
    return get_response


def insert_note(title, content, category):
    post_url = f'http://127.0.0.1:8888/insert'
    post_response = post_request(post_url, {'title': title, 'content': content, 'category': category})
    return post_response


def update_note(title, content, category):
    post_url = f'http://127.0.0.1:8888/update'
    post_response = post_request(post_url, {'title': title, 'content': content, 'category': category})
    return post_response


if __name__ == '__main__':
    query_note("第一篇笔记")

    insert_note("第二篇笔记", "第二篇笔记的内容", "")
    query_notes()
