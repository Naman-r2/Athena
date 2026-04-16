import { useState } from "react";
import { motion } from "framer-motion";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { Feather, Sparkles } from "lucide-react";
import PageLayout from "@/components/PageLayout";
import Loader from "@/components/Loader";
import ErrorMessage from "@/components/ErrorMessage";
import GreekDivider from "@/components/GreekDivider";
import { generateBlog, Blog } from "@/lib/api";

const Generate = () => {
  const [topic, setTopic] = useState("");
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: (t: string) => generateBlog(t),
    onSuccess: (data: Blog) => {
      navigate(`/blog/${data.id}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) mutation.mutate(topic.trim());
  };

  const suggestions = [
    "Docker containerization best practices",
    "Building REST APIs with FastAPI",
    "React performance optimization",
    "Introduction to WebAssembly",
  ];

  return (
    <PageLayout>
      <div className="max-w-2xl mx-auto px-4 py-14 sm:py-20">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-primary/10 mb-5">
            <Feather size={24} className="text-primary" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-heading font-bold text-secondary mb-2">
            Generate Blog
          </h1>
          <p className="text-sm text-muted-foreground font-body">
            Let AI create a technical article on any topic
          </p>
          <GreekDivider className="mt-5" />
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          onSubmit={handleSubmit}
          className="scroll-container p-8 sm:p-10"
        >
          <label
            htmlFor="topic"
            className="block text-sm font-body font-medium text-secondary mb-3"
          >
            What would you like to learn about?
          </label>
          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Building REST APIs with FastAPI"
            disabled={mutation.isPending}
            className="w-full px-4 py-3.5 rounded-lg bg-parchment/80 border border-gold/20 font-body text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/20 transition-all disabled:opacity-50"
          />

          {/* Suggestions */}
          {!topic && (
            <div className="mt-4 flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setTopic(s)}
                  className="text-xs font-body px-3 py-1.5 rounded-md border border-gold/15 text-muted-foreground hover:text-primary hover:border-gold/30 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          <button
            type="submit"
            disabled={!topic.trim() || mutation.isPending}
            className="mt-6 w-full flex items-center justify-center gap-2 py-3.5 rounded-lg bg-primary text-primary-foreground font-body font-medium text-sm hover:bg-primary/90 transition-all duration-200 disabled:opacity-40 active:scale-[0.99]"
          >
            <Sparkles size={16} />
            {mutation.isPending ? "Generating…" : "Generate Knowledge"}
          </button>
        </motion.form>

        {mutation.isPending && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-10"
          >
            <Loader text="The oracle is composing your article…" />
          </motion.div>
        )}

        {mutation.isError && (
          <div className="mt-8">
            <ErrorMessage
              message="Generation failed. Ensure the backend is running at localhost:8000."
              onRetry={() => mutation.mutate(topic.trim())}
            />
          </div>
        )}
      </div>
    </PageLayout>
  );
};

export default Generate;
