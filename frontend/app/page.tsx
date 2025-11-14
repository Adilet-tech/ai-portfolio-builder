"use client";

import React from "react";
import { Sparkles, Zap, Layout, Download } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      {/* Header */}
      <header className="absolute top-0 left-0 right-0 z-10">
        <nav className="container mx-auto px-6 py-6 flex justify-between items-center">
          <div className="text-2xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-8 h-8" />
            Foliomind
          </div>
          <div className="flex gap-4">
            <a
              href="/login"
              className="px-6 py-2 text-white hover:bg-white/10 rounded-lg transition"
            >
              Войти
            </a>
            <a
              href="/register"
              className="px-6 py-2 bg-white text-purple-900 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Начать
            </a>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 pt-32 pb-20">
        <div className="text-center max-w-4xl mx-auto">
          <div className="inline-block mb-6">
            <span className="bg-purple-500/20 text-purple-200 px-4 py-2 rounded-full text-sm font-semibold backdrop-blur-sm">
              ✨ Powered by AI
            </span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Создайте идеальное
            <span className="bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
              {" "}
              портфолио{" "}
            </span>
            за минуты
          </h1>

          <p className="text-xl text-purple-200 mb-10 leading-relaxed">
            AI Portfolio Builder использует искусственный интеллект для создания
            профессионального портфолио, которое выделит вас среди конкурентов
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/register"
              className="px-8 py-4 bg-white text-purple-900 rounded-xl font-bold text-lg hover:bg-gray-100 transition shadow-2xl"
            >
              Создать портфолио бесплатно
            </a>
            <button className="px-8 py-4 bg-purple-500/20 text-white rounded-xl font-bold text-lg hover:bg-purple-500/30 transition backdrop-blur-sm">
              Посмотреть примеры
            </button>
          </div>
        </div>

        {/* Preview Card */}
        <div className="mt-20 max-w-5xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20 shadow-2xl">
            <div className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl p-8 text-white">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-16 h-16 bg-white/20 rounded-full" />
                <div>
                  <div className="text-2xl font-bold">Иван Иванов</div>
                  <div className="text-purple-200">Full-Stack разработчик</div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="h-3 bg-white/30 rounded w-3/4" />
                <div className="h-3 bg-white/30 rounded w-1/2" />
                <div className="h-3 bg-white/30 rounded w-2/3" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-20">
        <h2 className="text-4xl font-bold text-white text-center mb-16">
          Почему выбирают Foliomind?
        </h2>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition">
            <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mb-6">
              <Sparkles className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">AI-генерация</h3>
            <p className="text-purple-200 leading-relaxed">
              Искусственный интеллект автоматически создаст уникальные описания
              ваших навыков и проектов
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition">
            <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mb-6">
              <Layout className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">
              Готовые шаблоны
            </h3>
            <p className="text-purple-200 leading-relaxed">
              Выбирайте из множества профессиональных дизайнов, созданных
              экспертами
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition">
            <div className="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center mb-6">
              <Download className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">Экспорт кода</h3>
            <p className="text-purple-200 leading-relaxed">
              Скачайте готовое портфолио в виде HTML/CSS и разместите где угодно
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-3xl mx-auto bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl p-12 shadow-2xl">
          <h2 className="text-4xl font-bold text-white mb-6">
            Готовы создать свое портфолио?
          </h2>
          <p className="text-xl text-purple-100 mb-8">
            Присоединяйтесь к тысячам профессионалов, которые уже создали своё
            идеальное портфолио с Foliomind
          </p>
          <a
            href="/register"
            className="inline-block px-10 py-4 bg-white text-purple-900 rounded-xl font-bold text-lg hover:bg-gray-100 transition shadow-xl"
          >
            Начать бесплатно
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-8 border-t border-white/10">
        <div className="text-center text-purple-300">
          <p>© 2024 Foliomind. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
}
