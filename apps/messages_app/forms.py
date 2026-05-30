from django import forms
from .models import AIConfig


class AIConfigForm(forms.ModelForm):
    class Meta:
        model = AIConfig
        fields = [
            'is_enabled', 'api_key', 'api_base_url', 'model_name',
            'system_prompt', 'temperature', 'max_tokens',
        ]
        widgets = {
            'api_key': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'sk-...',
            }),
            'api_base_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://api.openai.com/v1',
            }),
            'model_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'gpt-3.5-turbo',
            }),
            'system_prompt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '你是一个友善的AI助手，请用中文回答问题。',
            }),
            'is_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 2,
                'step': 0.1,
            }),
            'max_tokens': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 4096,
            }),
        }
