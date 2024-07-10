from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .models import Message
from .forms import MessageForm


class AdminConversationView(LoginRequiredMixin, View):
    def get(self, request, user_id=None):
        if user_id:
            user = User.objects.get(id=user_id)
            messages = (Message.objects.filter(
                sender=user,
                receiver=request.user
            ).select_related('sender') |
                        Message.objects.filter(
                            sender=request.user,
                            receiver=user
                        ).select_related('sender'))
            messages.filter(receiver=request.user).update(is_read=True)
            form = MessageForm()
            return render(
                request,
                'admin_conversation.html',
                {'messages': messages, 'form': form, 'user': user}
            )
        else:
            users = User.objects.filter(sent_messages__receiver=request.user).distinct()
            return render(
                request,
                'admin_user_list.html',
                {'users': users}
            )

    def post(self, request, user_id):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = User.objects.get(id=user_id)
            message.save()
            return redirect('admin_conversation', user_id=user_id)
        else:
            user = User.objects.get(id=user_id)
            messages = (Message.objects.filter(
                sender=user,
                receiver=request.user
            ).select_related('sender') |
                        Message.objects.filter(
                            sender=request.user,
                            receiver=user
                        ).select_related('sender')
                        )
            return render(
                request,
                'admin_conversation.html',
                {'messages': messages, 'form': form, 'user': user}
            )


class UserConversationView(LoginRequiredMixin, View):
    def get(self, request):
        messages = (Message.objects.filter(sender=request.user)
                    .select_related('sender') |
                    Message.objects.filter(receiver=request.user)
                    .select_related('sender'))
        messages = messages.order_by('timestamp')
        form = MessageForm()
        return render(request, 'user_conversation.html', {'messages': messages, 'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = User.objects.get(is_superuser=True)
            message.save()
            return redirect('user_conversation')
        else:
            messages = (Message.objects.filter(sender=request.user)
                        .select_related('sender') |
                        Message.objects.filter(receiver=request.user)
                        .select_related('sender'))
            messages = messages.order_by('timestamp')
            return render(
                request,
                'user_conversation.html',
                {'messages': messages, 'form': form}
            )
