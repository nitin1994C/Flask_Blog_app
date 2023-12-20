from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db


views = Blueprint("views", __name__)



@views.route("/create-post", methods=['POST'])
@login_required
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    title = data.get('title')
    content = data.get('content')

    if not title:
        return jsonify({"error": "Post cannot be empty it must have title"}), 400
    else:
        post = Post(title=title, content=content,author=current_user.id)
        db.session.add(post)
        db.session.commit()
        return jsonify({"message": "Post created successfully"}), 201
    



# Update Post route
@views.route('/update_post/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    data = request.get_json()
    new_title = data.get('title')
    new_content = data.get('content')

    post = Post.query.get(post_id)

    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Check if the current user is the author of the post
    if post.author != current_user:
        return jsonify({'message': 'You do not have permission to update this post'}), 403

    post.title = new_title
    post.content = new_content
    db.session.commit()

    return jsonify({'message': 'Post updated successfully'}), 200


# get all post

@views.route('/get_all_posts', methods=['GET'])
def all_posts():
    try:
        posts = Post.query.all()

        post_list = []
        for post in posts:
            post_data = {
            
                'title': post.title,
                'content': post.content,
                'date_created': post.date_created,
                'author': get_user_info(post.author),
                'comments': get_comments_for_post(post.id),
                'likes': get_likes_for_post(post.id)
            }
            post_list.append(post_data)

        return jsonify({'posts': post_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return { 'username': user.username}
    return None

def get_comments_for_post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_list = []
    for comment in comments:
        comment_list.append({
            'comment': comment.text,
            'date_commented': comment.date_created,
            'commented_by': get_user_info(comment.author)
        })
    return comment_list


def get_likes_for_post(post_id):
    likes_count = Like.query.filter_by(post_id=post_id).count()
    return likes_count

#### All POST BY perticular users


@views.route('/user_posts', methods=['GET'])
@login_required
def user_posts():
    try:
        user_id = request.args.get('user_id') or current_user.id

        posts = Post.query.filter_by(author=user_id).all()

        post_list = []
        for post in posts:
            post_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'date_created': post.date_created,
                'author': get_user_info(post.author),
                'comments': get_comments_for_post(post.id),
                'likes_count': get_likes_count_for_post(post.id)
            }
            post_list.append(post_data)

        return jsonify({'posts': post_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return {'id': user.id, 'username': user.username, 'email': user.email}
    return None


def get_comments_for_post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_list = []
    for comment in comments:
        comment_list.append({
            'id': comment.id,
            'text': comment.text,
            'date_created': comment.date_created,
            'author': get_user_info(comment.author)
        })
    return comment_list


def get_likes_count_for_post(post_id):
    likes = Like.query.filter_by(post_id=post_id).all()
    like_list = []
    for like in likes:
        like_list.append({
            'id': like.id,
            'date_created': like.date_created,
            'author': get_user_info(like.author)
        })
    return like_list


# DELETE POST

@views.route("/delete-post/<id>", methods=['DELETE'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        return jsonify({"error": "Post does not exist"}), 404
    elif current_user.id != post.id:
        return jsonify({"error": "You do not have permission to delete this post"}), 403
    else:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted successfully"}), 200


# CREATE COMMENT
    
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    text = data.get('text')

    if not text:
        return jsonify({"error": "Comment cannot be empty"}), 400
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return jsonify({"message": "Comment created successfully"}), 201
        else:
            return jsonify({"error": "Post does not exist"}), 404


@views.route("/delete-comment/<comment_id>", methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        return jsonify({"error": "Comment does not exist"}), 404
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        return jsonify({"error": "You do not have permission to delete this comment"}), 403
    else:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment deleted successfully"}), 200

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist'}, 404)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)}), 200

