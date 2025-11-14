"use client";

import React, { useState } from "react";
// Импорт компонентов UI (shadcn/ui) и иконок
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CheckCircle } from "lucide-react";

// Устанавливаем базовый URL API из переменной окружения
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });

  // 1. ИСПОЛЬЗУЕМ setError, который был объявлен вверху
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Обработчик изменения полей формы
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const validateForm = () => {
    // Сброс предыдущих ошибок
    setError("");

    if (!formData.email || !formData.password || !formData.confirmPassword) {
      setError("Все поля обязательны для заполнения");
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError("Введите корректный email адрес");
      return false;
    }

    if (formData.password.length < 6) {
      setError("Пароль должен содержать минимум 6 символов");
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Пароли не совпадают");
      return false;
    }

    return true;
  };

  const handleSubmit = async () => {
    setError("");

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // ⭐️ 1. ГЕНЕРИРУЕМ USERNAME ИЗ EMAIL
      const username = formData.email.split("@")[0];

      // 2. ОТПРАВЛЯЕМ ЗАПРОС С ДОБАВЛЕННЫМ USERNAME
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          username: username, // <--- ЭТО РЕШЕНИЕ
        }),
      });

      if (!response.ok) {
        let errorMessage = "Ошибка при регистрации.";
        try {
          const errorData = await response.json();
          // Дополнительная проверка на уникальность username/email
          if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
            errorMessage = errorData.detail[0].msg;
          } else if (typeof errorData.detail === "string") {
            errorMessage = errorData.detail;
          }
        } catch (e) {
          errorMessage = `Ошибка HTTP: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      setSuccess(true);

      // Перенаправляем на страницу входа через 2 секунды
      setTimeout(() => {
        window.location.href = "/login";
      }, 2000);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Неизвестная ошибка сети");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  // --- УСПЕШНЫЙ ВИД ---
  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100 p-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Регистрация успешна!
            </h2>
            <p className="text-gray-600 mb-4">
              Теперь вы можете войти в свой аккаунт
            </p>
            <div className="text-sm text-gray-500">
              Перенаправление на страницу входа...
            </div>
          </div>
        </div>
      </div>
    );
  }

  // --- ФОРМА РЕГИСТРАЦИИ ---
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-pink-100 p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Регистрация
            </h1>
            <p className="text-gray-600">Создайте аккаунт в Foliomind</p>
          </div>

          <div className="space-y-6">
            {/* Поле для отображения ошибки */}
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                placeholder="your@email.com"
                value={formData.email}
                onChange={handleChange}
                onKeyPress={handleKeyPress}
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Пароль
              </label>
              <input
                id="password"
                type="password"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                placeholder="Минимум 6 символов"
                value={formData.password}
                onChange={handleChange}
                onKeyPress={handleKeyPress}
              />
            </div>

            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Подтвердите пароль
              </label>
              <input
                id="confirmPassword"
                type="password"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                placeholder="Повторите пароль"
                value={formData.confirmPassword}
                onChange={handleChange}
                onKeyPress={handleKeyPress}
              />
            </div>

            <button
              onClick={handleSubmit}
              disabled={isLoading}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Регистрация..." : "Зарегистрироваться"}
            </button>
          </div>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Уже есть аккаунт?{" "}
              <a
                href="/login"
                className="text-purple-600 hover:text-purple-700 font-semibold"
              >
                Войти
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
