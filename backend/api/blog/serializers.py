from django.db.models import fields
from rest_framework import serializers
from blog.models import Post, Comment, Reply


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 
                'content', 'cover_photo', 
                'status', 'upvotes', 'downvotes',
        ]
        read_only_fields = ['author', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 
                'text', 'status', 'upvotes', 
                'downvotes',
        ]
        read_only_fields = ['author', 'post']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'author', 'comment', 
                'text', 'status', 'upvotes',
                'downvotes',
        ]
        read_only_fields = ['author', 'comment']
