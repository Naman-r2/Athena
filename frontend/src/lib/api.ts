import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 30000,
});

export interface Blog {
  id: string;
  title: string;
  content: string;
  tags: string[];
  preview: string;
  image_url?: string;
  created_at: string;
}

export interface SearchResult {
  id: string;
  title: string;
  preview: string;
  tags: string[];
}

export const fetchBlogs = async (): Promise<Blog[]> => {
  const { data } = await api.get("/blogs");
  return data;
};

export const fetchBlog = async (id: string): Promise<Blog> => {
  const { data } = await api.get(`/blogs/${id}`);
  return data;
};

export const searchBlogs = async (query: string): Promise<SearchResult[]> => {
  const { data } = await api.get("/search", { params: { q: query } });
  return data;
};

export const generateBlog = async (topic: string): Promise<Blog> => {
  const { data } = await api.post("/generate-blog", { topic });
  return data;
};

export const fetchRelatedBlogs = async (blogId: string): Promise<Blog[]> => {
  const { data } = await api.get(`/blogs/${blogId}/related`);
  return data;
};

export const chatWithPythia = async (question: string, blogId: string): Promise<{ answer: string }> => {
  const { data } = await api.post("/chat", { question, blog_id: blogId });
  return data;
};

export default api;
