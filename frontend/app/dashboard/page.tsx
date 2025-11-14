"use client";

import React, { useState, useEffect } from "react";
import { LogOut, Sparkles, Loader2 } from "lucide-react";

// Типы для портфолио
interface Project {
  name: string;
  description: string;
  technologies: string[];
}

interface PortfolioData {
  aboutMe: string;
  skills: string[];
  projects: Project[];
  generatedAbout?: string;
  generatedSkills?: { [category: string]: string[] };
  generatedProjects?: Array<{ name: string; description: string }>;
}

interface User {
  id: number;
  email: string;
  created_at: string;
}

function AIPortfolioGenerator({
  onGenerate,
}: {
  onGenerate: (data: PortfolioData) => void;
}) {
  const [aboutMe, setAboutMe] = useState("");
  const [skills, setSkills] = useState("");
  const [projects, setProjects] = useState<Project[]>([
    { name: "", description: "", technologies: [] },
  ]);
  const [isGenerating, setIsGenerating] = useState(false);

  const addProject = () => {
    setProjects([...projects, { name: "", description: "", technologies: [] }]);
  };

  const updateProject = (
    index: number,
    field: keyof Project,
    value: string | string[]
  ) => {
    const newProjects = [...projects];
    newProjects[index] = { ...newProjects[index], [field]: value };
    setProjects(newProjects);
  };

  const handleGenerate = async () => {
    setIsGenerating(true);

    // Имитация AI генерации (замените на реальный API)
    setTimeout(() => {
      const data: PortfolioData = {
        aboutMe,
        skills: skills.split(",").map((s) => s.trim()),
        projects,
        generatedAbout: `Привет! Я ${aboutMe}. Опытный специалист с глубокими знаниями в современных технологиях. 
        Мне нравится создавать инновационные решения и работать над интересными проектами. 
        Постоянно изучаю новые технологии и совершенствую свои навыки.`,
        generatedSkills: {
          Frontend: skills
            .split(",")
            .slice(0, 3)
            .map((s) => s.trim()),
          Backend: skills
            .split(",")
            .slice(3, 6)
            .map((s) => s.trim()),
          Tools: skills
            .split(",")
            .slice(6)
            .map((s) => s.trim()),
        },
        generatedProjects: projects.map((p) => ({
          name: p.name,
          description: `${
            p.description
          } Этот проект демонстрирует мой опыт работы с ${p.technologies.join(
            ", "
          )}. 
          Успешно реализованы все ключевые функции с применением лучших практик разработки.`,
        })),
      };

      onGenerate(data);
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
        <Sparkles className="w-6 h-6 text-purple-600" />
        Генератор портфолио
      </h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Обо мне (ключевые слова)
          </label>
          <textarea
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            rows={3}
            placeholder="Frontend разработчик, увлекаюсь созданием современных веб-приложений..."
            value={aboutMe}
            onChange={(e) => setAboutMe(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Навыки (через запятую)
          </label>
          <input
            type="text"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            placeholder="React, TypeScript, Node.js, PostgreSQL..."
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
          />
        </div>

        <div className="space-y-3">
          <label className="block text-sm font-medium text-gray-700">
            Проекты
          </label>
          {projects.map((project, index) => (
            <div
              key={index}
              className="p-4 border border-gray-200 rounded-lg space-y-3"
            >
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                placeholder="Название проекта"
                value={project.name}
                onChange={(e) => updateProject(index, "name", e.target.value)}
              />
              <textarea
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                rows={2}
                placeholder="Краткое описание"
                value={project.description}
                onChange={(e) =>
                  updateProject(index, "description", e.target.value)
                }
              />
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                placeholder="Технологии (через запятую)"
                value={project.technologies.join(", ")}
                onChange={(e) =>
                  updateProject(
                    index,
                    "technologies",
                    e.target.value.split(",").map((t) => t.trim())
                  )
                }
              />
            </div>
          ))}
          <button
            onClick={addProject}
            className="text-purple-600 hover:text-purple-700 font-medium text-sm"
          >
            + Добавить проект
          </button>
        </div>

        <button
          onClick={handleGenerate}
          disabled={isGenerating || !aboutMe || !skills}
          className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Генерация...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Сгенерировать портфолио
            </>
          )}
        </button>
      </div>
    </div>
  );
}

function PortfolioPreview({ data }: { data: PortfolioData | null }) {
  if (!data) {
    return (
      <div className="bg-gray-50 rounded-xl shadow-lg p-12 text-center">
        <div className="max-w-md mx-auto">
          <div className="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Ваше портфолио появится здесь
          </h3>
          <p className="text-gray-500">
            Заполните форму слева и нажмите "Сгенерировать"
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Обо мне</h2>
        <p className="text-gray-700 leading-relaxed">{data.generatedAbout}</p>
      </div>

      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Навыки</h2>
        <div className="space-y-4">
          {data.generatedSkills &&
            Object.entries(data.generatedSkills).map(([category, skills]) => (
              <div key={category}>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  {category}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
        </div>
      </div>

      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Проекты</h2>
        <div className="space-y-6">
          {data.generatedProjects?.map((project, i) => (
            <div key={i} className="border border-gray-200 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {project.name}
              </h3>
              <p className="text-gray-700">{project.description}</p>
            </div>
          ))}
        </div>
      </div>

      <button className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition">
        Опубликовать портфолио
      </button>
    </div>
  );
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [portfolioData, setPortfolioData] = useState<PortfolioData | null>(
    null
  );

  useEffect(() => {
    // Проверка токена при загрузке
    const token = localStorage.getItem("access_token");

    if (!token) {
      setIsLoading(false);
      window.location.href = "/login";
      return;
    }

    // Получение данных пользователя
    fetch("http://localhost:8000/api/v1/users/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Unauthorized");
        return res.json();
      })
      .then((data) => {
        setUser(data);
        setIsLoading(false);
      })
      .catch(() => {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
      });
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Foliomind</h1>
            <p className="text-sm text-gray-600">{user.email}</p>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition"
          >
            <LogOut className="w-4 h-4" />
            Выйти
          </button>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          <AIPortfolioGenerator onGenerate={setPortfolioData} />
          <PortfolioPreview data={portfolioData} />
        </div>
      </main>
    </div>
  );
}
