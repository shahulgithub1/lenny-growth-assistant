import axios, { AxiosInstance } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Source {
  episode_title: string;
  guest?: string;
  excerpt: string;
  chunk_id: string;
  source_file: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  created_at: string;
  metadata?: {
    model_provider?: string;
    model_name?: string;
    retrieval_count?: number;
    generation_time_ms?: number;
  };
}

export interface Session {
  id: string;
  created_at: string;
  updated_at: string;
  title?: string;
  message_count?: number;
  messages?: Message[];
}

export interface Artifact {
  id: string;
  session_id: string;
  message_id?: string;
  type: 'markdown' | 'html' | 'css';
  content: string;
  created_at: string;
  metadata?: {
    title?: string;
    description?: string;
    size_bytes?: number;
  };
}

export interface CreateMessageRequest {
  content: string;
  model_provider?: string;
}

export interface CreateMessageResponse extends Message {}

export interface HealthResponse {
  status: string;
  database?: string;
  ollama?: string;
  timestamp: string;
  service?: string;
  version?: string;
}

export class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = API_URL) {
    this.client = axios.create({
      baseURL: `${baseURL}/api`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 120000, // 2 minutes for LLM responses
    });
  }

  // Health
  async checkHealth(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  // Sessions
  async createSession(): Promise<Session> {
    const response = await this.client.post<Session>('/sessions', {});
    return response.data;
  }

  async listSessions(limit = 50, offset = 0): Promise<{ sessions: Session[]; total: number }> {
    const response = await this.client.get<{ sessions: Session[]; total: number; limit: number; offset: number }>(
      '/sessions',
      { params: { limit, offset } }
    );
    return response.data;
  }

  async getSession(sessionId: string): Promise<Session> {
    const response = await this.client.get<Session>(`/sessions/${sessionId}`);
    return response.data;
  }

  async deleteSession(sessionId: string): Promise<void> {
    await this.client.delete(`/sessions/${sessionId}`);
  }

  // Messages
  async sendMessage(sessionId: string, request: CreateMessageRequest): Promise<CreateMessageResponse> {
    const response = await this.client.post<any>(
      `/sessions/${sessionId}/messages`,
      request
    );
    const msg = response.data;
    if (msg && msg.message_metadata && !msg.metadata) {
      msg.metadata = msg.message_metadata;
    }
    return msg;
  }

  // Artifacts
  async getArtifact(artifactId: string): Promise<Artifact> {
    const response = await this.client.get<Artifact>(`/artifacts/${artifactId}`);
    return response.data;
  }

  async listArtifacts(sessionId: string): Promise<Artifact[]> {
    const response = await this.client.get<Artifact[]>(`/sessions/${sessionId}/artifacts`);
    return response.data;
  }
}

export const apiClient = new ApiClient();
