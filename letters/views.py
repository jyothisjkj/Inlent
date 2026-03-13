from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Letter
from .forms import LetterAddressForm, LetterContentForm


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = "letters/letter_list.html"
    context_object_name = "letters"

    def get_queryset(self):
        return Letter.objects.filter(user=self.request.user, is_sent=True)


class LetterAddressCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterAddressForm
    template_name = "letters/letter_address_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Handle "Send to Self" logic
        if form.cleaned_data.get("send_to_self"):
            form.instance.receiver_fullname = form.instance.sender_fullname
            form.instance.receiver_nickname = form.instance.sender_nickname
            form.instance.receiver_place = form.instance.sender_place
            form.instance.receiver_city = form.instance.sender_city
            form.instance.receiver_state = form.instance.sender_state
            form.instance.receiver_country = form.instance.sender_country
            form.instance.receiver_pincode = form.instance.sender_pincode

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("letters:create_content", kwargs={"pk": self.object.pk})


class LetterContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterContentForm
    template_name = "letters/letter_content_form.html"
    success_url = reverse_lazy("letters:list")

    def get_queryset(self):
        return Letter.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.is_sent = True
        return super().form_valid(form)
