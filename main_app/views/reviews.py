from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Game, Review


@login_required
def add_review(request, game_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = int(request.POST.get('rating') or 0)
        game = get_object_or_404(Game, id=game_id)

        review = Review(
            content=content,
            rating=rating,
            user=request.user,
            game=game
        )
        review.save()
        return redirect('games_detail', pk=game_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        review.delete()

    return redirect('games_detail', pk=review.game.id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        rating = int(request.POST.get('rating') or 0)
        
        review.content = content
        review.rating = rating
        review.save()

        return redirect('games_detail', pk=review.game.id)
    else:
        return render(request, 'edit-modal.html', {'review': review})
