import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    global POSTS
    sort = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    if sort is None :
        return jsonify(POSTS)
    if sort not in {'title', 'content'} or direction not in {'asc', 'desc'}:
        return jsonify({'message': 'Invalid input'}), 400

    if direction == 'asc':
        sorted_posts = sorted(POSTS, key=lambda x: x.get(sort, ''))
    else:
        sorted_posts = sorted(POSTS, key=lambda x: x.get(sort, ''), reverse=True)
    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    post_id = str(uuid.uuid4())
    if title is None or content is None:
        return jsonify({'error': 'Missing title or content'}), 400
    new_post = {'Id': post_id, 'title': title, 'content': content}
    POSTS.append(new_post)
    return jsonify(POSTS), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    posts_ids = [post['id'] for post in POSTS]
    if post_id not in posts_ids:
        return jsonify({'message': "there is no post with this id"}), 404
    POSTS = [post for post in POSTS if post['id'] != post_id]
    return jsonify({'message': f"the post with id number : {post_id} has been removed"}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    global POSTS
    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if post_to_update is None:
        return jsonify({'message': "there is no post with this id"}), 404
    data = request.get_json()
    if 'title' in data:
        post_to_update['title'] = data['title']
    if 'content' in data:
        post_to_update['content'] = data['content']
    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    global POSTS
    title = request.args.get('title')
    content = request.args.get('content')
    posts_with_search = [post for post in POSTS if
                         (title.lower() in post['title'].lower() if title else True) and
                         (content.lower() in post['content'].lower() if content else True)]
    return jsonify(posts_with_search)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
