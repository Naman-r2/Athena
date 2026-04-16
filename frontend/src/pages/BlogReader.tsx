import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { ArrowLeft, Calendar, Tag, Send, MessageCircle } from "lucide-react";
import PageLayout from "@/components/PageLayout";
import BlogCard from "@/components/BlogCard";
import Loader from "@/components/Loader";
import ErrorMessage from "@/components/ErrorMessage";
import GreekDivider from "@/components/GreekDivider";
import { fetchBlog, chatWithPythia, fetchRelatedBlogs } from "@/lib/api";
import { useState } from "react";
import api from "../services/api";

const BlogReader = () => {
  const { id } = useParams<{ id: string }>();
  const { data: blog, isLoading, isError, refetch } = useQuery({
    queryKey: ["blog", id],
    queryFn: () => fetchBlog(id!),
    enabled: !!id,
    retry: 1,
  });

  const { data: relatedBlogs } = useQuery({
    queryKey: ["related-blogs", id],
    queryFn: () => fetchRelatedBlogs(id!),
    enabled: !!id,
    retry: 1,
  });

  const [chatMessages, setChatMessages] = useState<Array<{question: string, answer: string}>>([]);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [isChatting, setIsChatting] = useState(false);

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuestion.trim() || !id) return;

    const question = currentQuestion.trim();
    setCurrentQuestion("");
    setIsChatting(true);

    try {
      const response = await chatWithPythia(question, id);
      setChatMessages(prev => [...prev, { question, answer: response.answer }]);
    } catch (error) {
      console.error("Chat error:", error);
      setChatMessages(prev => [...prev, { question, answer: "Sorry, I encountered an error. Please try again." }]);
    } finally {
      setIsChatting(false);
    }
  };

  return (
    <PageLayout>
      <div className="max-w-3xl mx-auto px-4 py-10 sm:py-14">
        {/* Back link */}
        <Link
          to="/library"
          className="inline-flex items-center gap-1.5 text-sm font-body text-muted-foreground hover:text-primary transition-colors mb-8"
        >
          <ArrowLeft size={14} />
          Back to Library
        </Link>

        {isLoading && <Loader text="Retrieving scroll…" />}
        {isError && <ErrorMessage message="Could not retrieve this article." onRetry={() => refetch()} />}

        {blog && (
          <motion.article
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            {/* Header */}
            <header className="mb-8">
              <h1 className="text-3xl sm:text-4xl font-heading font-bold text-secondary leading-tight mb-4">
                {blog.title}
              </h1>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted-foreground font-body">
                <span className="flex items-center gap-1">
                  <Calendar size={12} />
                  {new Date(blog.created_at).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })}
                </span>
                {blog.tags.length > 0 && (
                  <span className="flex items-center gap-1">
                    <Tag size={12} />
                    {blog.tags.join(", ")}
                  </span>
                )}
              </div>
              <GreekDivider className="mt-6" />
            </header>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-8">
              {blog.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs font-body font-medium px-3 py-1 rounded bg-primary/8 text-primary border border-primary/15"
                >
                  {tag}
                </span>
              ))}
            </div>

            {/* Content */}
            <div className="scroll-container p-8 sm:p-12">
              {/* Blog Image */}
              {blog.image_url && (
                <div className="mb-8">
                  <img
                    src={blog.image_url}
                    alt={blog.title}
                    className="w-full max-w-2xl mx-auto rounded-lg shadow-lg"
                  />
                </div>
              )}
              
              <div
                className="prose prose-stone max-w-none font-body text-foreground leading-[1.8]
                  prose-headings:font-heading prose-headings:text-secondary prose-headings:mt-8 prose-headings:mb-4
                  prose-p:mb-4
                  prose-code:bg-secondary/8 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:font-mono
                  prose-pre:bg-secondary prose-pre:text-secondary-foreground prose-pre:rounded prose-pre:p-4 prose-pre:overflow-x-auto
                  prose-a:text-primary prose-a:no-underline hover:prose-a:underline
                  prose-strong:text-secondary
                  prose-blockquote:border-l-gold prose-blockquote:text-muted-foreground prose-blockquote:italic"
                dangerouslySetInnerHTML={{ __html: blog.content }}
              />
            </div>
          </motion.article>
        )}

        {/* Pythia Chat Section */}
        {blog && (
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-12"
          >
            <GreekDivider className="mb-8" />
            <div className="text-center mb-8">
              <MessageCircle size={32} className="mx-auto text-primary mb-2" />
              <h2 className="text-2xl font-heading font-bold text-secondary mb-2">
                Consult Pythia
              </h2>
              <p className="text-sm text-muted-foreground font-body">
                Ask questions about this article and receive wisdom from the oracle
              </p>
            </div>

            {/* Chat Messages */}
            {chatMessages.length > 0 && (
              <div className="max-w-3xl mx-auto mb-6 space-y-4">
                {chatMessages.map((msg, index) => (
                  <div key={index} className="space-y-2">
                    <div className="flex justify-end">
                      <div className="bg-primary text-primary-foreground px-4 py-2 rounded-lg max-w-md">
                        <p className="text-sm font-body">{msg.question}</p>
                      </div>
                    </div>
                    <div className="flex justify-start">
                      <div className="bg-secondary text-secondary-foreground px-4 py-2 rounded-lg max-w-2xl">
                        <p className="text-sm font-body leading-relaxed">{msg.answer}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Chat Input */}
            <form onSubmit={handleChatSubmit} className="max-w-2xl mx-auto">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={currentQuestion}
                  onChange={(e) => setCurrentQuestion(e.target.value)}
                  placeholder="Ask Pythia about this article..."
                  className="flex-1 px-4 py-3 rounded-lg bg-parchment border border-gold/20 font-body text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/20"
                  disabled={isChatting}
                />
                <button
                  type="submit"
                  disabled={isChatting || !currentQuestion.trim()}
                  className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-body font-medium hover:bg-primary/90 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {isChatting ? (
                    <Loader text="" />
                  ) : (
                    <Send size={16} />
                  )}
                  Ask
                </button>
              </div>
            </form>
          </motion.div>
        )}

        {/* Related Blogs */}
        {relatedBlogs && relatedBlogs.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-12"
          >
            <GreekDivider className="mb-8" />
            <div className="text-center mb-8">
              <h2 className="text-2xl font-heading font-bold text-secondary mb-2">
                Related Scrolls
              </h2>
              <p className="text-sm text-muted-foreground font-body">
                Other writings that may interest you
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 max-w-5xl mx-auto">
              {relatedBlogs.slice(0, 6).map((relatedBlog, i) => (
                <BlogCard
                  key={relatedBlog.id}
                  id={relatedBlog.id}
                  title={relatedBlog.title}
                  preview={relatedBlog.preview}
                  tags={relatedBlog.tags}
                  imageUrl={relatedBlog.image_url}
                  date={new Date(relatedBlog.created_at).toLocaleDateString()}
                  index={i}
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </PageLayout>
  );
};

export default BlogReader;
