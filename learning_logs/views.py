from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.http import Http404

from .models import Topic, Entry

from .forms import TopicForm, EntryForm


def index(request):
    """the home page for the learning log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def contents(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    contents = []
    for topic in topics:
        content = topic.entry_set.order_by('-date_added')
        contents.append(content)
    context = {'contents':contents}
    return render(request, 'learning_logs/contents.html', context)



@login_required
def topic(request, topic_id):
    """show a single topic and all  its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    #Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # no data submitted, creat a blank form.
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = get_object_or_404(Topic ,id=topic_id)
    #Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted,  create a blank form.
        form = EntryForm()
    else:
        # Post data submitted, process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry ,id=entry_id)
    topic = entry.topic
    #Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # initial request; prefill form with current entry.
        form = EntryForm(instance=entry)
    else:
        # post data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    """delete an existing entry."""
    topic = get_object_or_404(Topic, id=topic_id)
    #make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    if request.method == "POST":
        topic.delete()
        return HttpResponseRedirect('/topics')
    context = {'topic':topic}
    return render(request, 'learning_logs/delete_topic.html', context)


@login_required
def delete_entry(request, entry_id):
    """delete an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    #make sure the entry belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    if request.method == "POST":
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'topic':topic, 'entry':entry}
    return render(request, 'learning_logs/delete_entry.html', context)


@login_required
def edit_topic(request, topic_id):
    """edit an existing topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    # make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_topic.html', context)


def about(request):
    """showing help information."""
    return render(request, 'learning_logs/about.html')

