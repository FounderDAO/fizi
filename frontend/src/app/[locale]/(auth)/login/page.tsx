'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function LoginPage() {
  const t = useTranslations('auth');
  const router = useRouter();
  const [step, setStep] = useState<'phone' | 'otp'>('phone');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendOTP = async () => {
    setLoading(true);
    setError('');
    try {
      await api.post('/auth/send-otp/', { phone });
      setStep('otp');
    } catch (e: any) {
      setError(e.response?.data?.error || 'Ошибка отправки кода');
    } finally {
      setLoading(false);
    }
  };

  const verifyOTP = async () => {
    setLoading(true);
    setError('');
    try {
      const { data } = await api.post('/auth/verify-otp/', { phone, code: otp });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      router.push('/');
    } catch (e: any) {
      setError(e.response?.data?.error || 'Неверный код');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-8">{t('login_title')}</h1>

        {step === 'phone' ? (
          <div className="space-y-4">
            <input
              type="tel"
              placeholder={t('phone_placeholder')}
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full border rounded-xl px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button
              onClick={sendOTP}
              disabled={loading || !phone}
              className="w-full bg-indigo-600 text-white rounded-xl py-3 font-semibold hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Отправка...' : t('send_code')}
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-center text-gray-600">Код отправлен на {phone}</p>
            <input
              type="text"
              placeholder="123456"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              maxLength={6}
              className="w-full border rounded-xl px-4 py-3 text-2xl text-center tracking-widest focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            {error && <p className="text-red-500 text-sm text-center">{error}</p>}
            <button
              onClick={verifyOTP}
              disabled={loading || otp.length !== 6}
              className="w-full bg-indigo-600 text-white rounded-xl py-3 font-semibold hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Проверка...' : t('verify')}
            </button>
            <button
              onClick={() => setStep('phone')}
              className="w-full text-gray-500 text-sm"
            >
              Изменить номер
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
