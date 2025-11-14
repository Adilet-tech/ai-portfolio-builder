/**
 * TypeScript типы для всего приложения
 */

// ============================================
// AUTH TYPES
// ============================================

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  avatar_url?: string;
  bio?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// ============================================
// PORTFOLIO TYPES
// ============================================

export interface Project {
  name: string;
  technologies: string[];
  brief_description?: string;
  url?: string;
  github_url?: string;
}

export interface GeneratedProject extends Project {
  description: string;
}

export interface SkillsStructure {
  [category: string]: string[];
}

export interface Portfolio {
  id: number;
  user_id: number;
  about_me?: string;
  headline?: string;
  skills_structured?: SkillsStructure;
  projects?: GeneratedProject[];
  work_experience?: WorkExperience[];
  education?: Education[];
  contact_info?: ContactInfo;
  template_id?: string;
  theme?: string;
  color_scheme?: ColorScheme;
  is_published: boolean;
  slug?: string;
  views_count: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
  meta_title?: string;
  meta_description?: string;
}

export interface WorkExperience {
  company: string;
  position: string;
  start_date: string;
  end_date?: string;
  description: string;
  technologies?: string[];
}

export interface Education {
  institution: string;
  degree: string;
  field: string;
  start_date: string;
  end_date?: string;
  description?: string;
}

export interface ContactInfo {
  email?: string;
  phone?: string;
  linkedin?: string;
  github?: string;
  twitter?: string;
  website?: string;
}

export interface ColorScheme {
  primary?: string;
  secondary?: string;
  accent?: string;
  background?: string;
  text?: string;
}

// ============================================
// AI GENERATION TYPES
// ============================================

export interface GenerateAboutRequest {
  name: string;
  skills: string[];
  experience_years?: number;
  industry?: string;
}

export interface GenerateProjectRequest {
  project_name: string;
  technologies: string[];
  brief_description?: string;
}

export interface GenerateFullPortfolioRequest {
  name: string;
  skills: string[];
  experience_years?: number;
  industry?: string;
  projects: Project[];
}

export interface GenerationResponse {
  success: boolean;
  content?: string;
  structure?: SkillsStructure;
  portfolio_id?: number;
}

export interface FullPortfolioResponse {
  success: boolean;
  portfolio_id: number;
  content: {
    headline?: string;
    about?: string;
    projects?: GeneratedProject[];
    skills_structure?: SkillsStructure;
  };
}

// ============================================
// API TYPES
// ============================================

export interface ApiError {
  detail: string | { msg: string; type: string }[];
}

export interface RateLimitHeaders {
  "x-ratelimit-limit-minute": string;
  "x-ratelimit-remaining-minute": string;
  "x-ratelimit-limit-hour": string;
  "x-ratelimit-remaining-hour": string;
}

// ============================================
// FORM TYPES
// ============================================

export interface ProjectFormData {
  name: string;
  technologies: string[];
  brief_description: string;
  url: string;
  github_url: string;
}

export interface PortfolioFormData {
  name: string;
  skills: string[];
  experience_years: string;
  industry: string;
  projects: ProjectFormData[];
}

// ============================================
// UI STATE TYPES
// ============================================

export type LoadingState = "idle" | "loading" | "success" | "error";

export interface GenerationState {
  status: LoadingState;
  error?: string;
  data?: FullPortfolioResponse;
}
