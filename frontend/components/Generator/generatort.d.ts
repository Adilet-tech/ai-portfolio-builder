// --- frontend/types/generator.d.ts (или types/index.ts) ---

interface Project {
  name: string;
  description: string;
  technologies: string[];
}

// Тип для данных, возвращаемых бэкендом
interface PortfolioData {
  aboutMe: string;
  skills: string[];
  projects: Project[];
  id: number;
  aboutMeText: string;
  skillsStructure: { [category: string]: string[] };
  projectDescriptions: Array<{ name: string; description: string }>;
  is_published: boolean;
}

// Тип для ответа публикации (для API client)
interface PublishResponse {
  success: boolean;
  is_published: boolean;
  message: string;
}
