'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useLocale } from 'next-intl';
import { ChevronRight, ChevronLeft, Upload, X, Sparkles, Loader2 } from 'lucide-react';
import api from '@/lib/api';

const STEPS = ['Категория', 'Фото', 'Описание', 'Цена'];
const CITIES = ['Ташкент', 'Самарканд', 'Бухара', 'Наманган', 'Андижан', 'Фергана', 'Нукус', 'Карши', 'Термез', 'Гулистан'];

export default function CreateListingPage() {
  const locale = useLocale();
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');
  const [categories, setCategories] = useState<any[]>([]);
  const [categoryId, setCategoryId] = useState<number | null>(null);
  const [photos, setPhotos] = useState<File[]>([]);
  const [photoPreviews, setPhotoPreviews] = useState<string[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [condition, setCondition] = useState('used');
  const [price, setPrice] = useState('');
  const [currency, setCurrency] = useState('UZS');
  const [city, setCity] = useState('Ташкент');
  const [aiSuggestion, setAiSuggestion] = useState<any>(null);

  useEffect(() => {
    api.get('/categories/').then(res => setCategories(res.data));
  }, []);

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const newPhotos = [...photos, ...files].slice(0, 10);
    setPhotos(newPhotos);
    setPhotoPreviews(newPhotos.map(f => URL.createObjectURL(f)));
  };

  const removePhoto = (index: number) => {
    const p = photos.filter((_, i) => i !== index);
    setPhotos(p);
    setPhotoPreviews(p.map(f => URL.createObjectURL(f)));
  };

  const getAISuggestion = async () => {
    if (!title) return;
    setAiLoading(true);
    try {
      const res = await api.post('/ai/suggest/', { title, description });
      setAiSuggestion(res.data);
      if (res.data.price_min && !price) {
        setPrice(String(Math.round((res.data.price_min + res.data.price_max) / 2)));
      }
    } catch {}
    finally { setAiLoading(false); }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
      formData.append('price', price);
      formData.append('currency', currency);
      formData.append('city', city);
      formData.append('condition', condition);
      if (categoryId) formData.append('category_id', String(categoryId));
      photos.forEach(photo => formData.append('uploaded_photos', photo));
      const res = await api.post('/listings/create/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      router.push(`/${locale}/listings/${res.data.id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Ошибка при создании');
    } finally { setLoading(false); }
  };

  const canNext = () => {
    if (step === 0) return categoryId !== null;
    if (step === 2) return title.length >= 3 && description.length >= 10;
    if (step === 3) return price.length > 0;
    return true;
  };

  const fmt = (n: number) => new Intl.NumberFormat('ru-RU').format(n);

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Подать объявление</h1>

      {/* Steps */}
      <div className="flex items-center gap-2 mb-8">
        {STEPS.map((s, i) => (
          <div key={i} className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
              i < step ? 'bg-green-500 text-white' : i === step ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-500'
            }`}>{i < step ? '✓' : i + 1}</div>
            <span className={`text-sm hidden sm:block ${i === step ? 'font-semibold' : 'text-gray-400'}`}>{s}</span>
            {i < STEPS.length - 1 && <div className="w-8 h-px bg-gray-300" />}
          </div>
        ))}
      </div>

      {/* Step 0: Category */}
      {step === 0 && (
        <div className="grid grid-cols-3 gap-3">
          {categories.map(cat => (
            <button key={cat.id} onClick={() => setCategoryId(cat.id)}
              className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                categoryId === cat.id ? 'border-indigo-600 bg-indigo-50' : 'border-gray-200 hover:border-gray-300'
              }`}>
              <span className="text-3xl">{cat.icon}</span>
              <span className="text-xs text-center font-medium">{cat.name_ru}</span>
            </button>
          ))}
        </div>
      )}

      {/* Step 1: Photos */}
      {step === 1 && (
        <div>
          <p className="text-gray-500 text-sm mb-4">До 10 фото. Первое — обложка.</p>
          <div className="grid grid-cols-3 gap-3">
            {photoPreviews.map((src, i) => (
              <div key={i} className="relative h-28 rounded-xl overflow-hidden border">
                <img src={src} className="w-full h-full object-cover" alt="" />
                <button onClick={() => removePhoto(i)} className="absolute top-1 right-1 bg-black/50 rounded-full p-1">
                  <X className="w-3 h-3 text-white" />
                </button>
                {i === 0 && <span className="absolute bottom-1 left-1 bg-indigo-600 text-white text-xs px-2 py-0.5 rounded-full">Обложка</span>}
              </div>
            ))}
            {photos.length < 10 && (
              <label className="h-28 border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:border-indigo-400">
                <Upload className="w-6 h-6 text-gray-400 mb-1" />
                <span className="text-xs text-gray-400">Добавить</span>
                <input type="file" accept="image/*" multiple className="hidden" onChange={handlePhotoUpload} />
              </label>
            )}
          </div>
        </div>
      )}

      {/* Step 2: Description */}
      {step === 2 && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Заголовок *</label>
            <input value={title} onChange={e => setTitle(e.target.value)}
              placeholder="Например: iPhone 13 128GB"
              className="w-full border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Описание *</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)}
              placeholder="Состояние, комплектация, причина продажи..."
              rows={5} className="w-full border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none" />
          </div>
          <div className="flex gap-3">
            {[['new', 'Новое'], ['used', 'Б/у']].map(([val, label]) => (
              <button key={val} onClick={() => setCondition(val)}
                className={`flex-1 py-2 rounded-xl border-2 font-medium text-sm transition-all ${
                  condition === val ? 'border-indigo-600 bg-indigo-50 text-indigo-700' : 'border-gray-200 text-gray-600'
                }`}>{label}</button>
            ))}
          </div>
          {title.length >= 3 && (
            <button onClick={getAISuggestion} disabled={aiLoading}
              className="flex items-center gap-2 text-indigo-600 text-sm font-medium hover:text-indigo-800">
              {aiLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              AI подсказка по цене
            </button>
          )}
          {aiSuggestion && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-3 text-sm">
              <p className="font-medium text-indigo-700">🤖 AI рекомендует:</p>
              <p className="text-gray-700 mt-1">
                Цена: {fmt(aiSuggestion.price_min)} — {fmt(aiSuggestion.price_max)} сум
              </p>
            </div>
          )}
        </div>
      )}

      {/* Step 3: Price */}
      {step === 3 && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Цена *</label>
            <div className="flex gap-2">
              <input value={price} onChange={e => setPrice(e.target.value)}
                type="number" placeholder="0"
                className="flex-1 border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              <select value={currency} onChange={e => setCurrency(e.target.value)}
                className="border rounded-xl px-3 py-3">
                <option value="UZS">UZS</option>
                <option value="USD">USD</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Город *</label>
            <select value={city} onChange={e => setCity(e.target.value)}
              className="w-full border rounded-xl px-4 py-3">
              {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        {step > 0 ? (
          <button onClick={() => setStep(s => s - 1)}
            className="flex items-center gap-2 px-6 py-3 border rounded-xl text-gray-600 hover:bg-gray-50">
            <ChevronLeft className="w-5 h-5" /> Назад
          </button>
        ) : <div />}
        {step < STEPS.length - 1 ? (
          <button onClick={() => setStep(s => s + 1)} disabled={!canNext()}
            className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-xl font-semibold disabled:opacity-50 hover:bg-indigo-700">
            Далее <ChevronRight className="w-5 h-5" />
          </button>
        ) : (
          <button onClick={handleSubmit} disabled={loading || !canNext()}
            className="flex items-center gap-2 px-8 py-3 bg-green-600 text-white rounded-xl font-semibold disabled:opacity-50 hover:bg-green-700">
            {loading && <Loader2 className="w-5 h-5 animate-spin" />}
            Опубликовать
          </button>
        )}
      </div>
    </div>
  );
}
