import { useNavigate, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { BookOpen, Feather, ArrowRight } from "lucide-react";
import PageLayout from "@/components/PageLayout";
import SearchBar from "@/components/SearchBar";
import BlogCard from "@/components/BlogCard";
import Loader from "@/components/Loader";
import GreekDivider from "@/components/GreekDivider";
import heroBg from "@/assets/hero-bg.jpg";
import athenaLogo from "@/assets/athena-logo.png";
import { fetchBlogs } from "@/lib/api";

const Home = () => {
  const navigate = useNavigate();
  const { data: blogs, isLoading, isError } = useQuery({
    queryKey: ["blogs"],
    queryFn: fetchBlogs,
    retry: 1,
  });

  const handleSearch = (q: string) => navigate(`/search?q=${encodeURIComponent(q)}`);
  const featured = blogs?.slice(0, 6);

  return (
    <PageLayout>
      {/* Hero */}
      <section className="relative overflow-hidden min-h-[70vh] flex items-center">
        <div className="absolute inset-0">
          <img src={heroBg} alt="" className="w-full h-full object-cover" width={1920} height={1080} />
          <div className="absolute inset-0 bg-gradient-to-b from-background/40 via-background/70 to-background" />
        </div>

        <div className="relative w-full max-w-4xl mx-auto px-4 py-24 sm:py-32 text-center">
          <motion.img
            src={athenaLogo}
            alt="Athena owl"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="w-16 h-16 mx-auto mb-6 drop-shadow-lg"
          />
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl sm:text-7xl font-heading font-bold text-secondary mb-2 tracking-tight"
          >
            Athena
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-base sm:text-lg text-muted-foreground font-body mb-3 tracking-widest uppercase"
          >
            Library of Technical Knowledge
          </motion.p>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <GreekDivider className="mb-8" />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <SearchBar onSearch={handleSearch} size="large" placeholder="Search for knowledge…" />
          </motion.div>

          {/* Quick actions */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="flex items-center justify-center gap-4 mt-8"
          >
            <Link
              to="/library"
              className="flex items-center gap-1.5 px-4 py-2 rounded-md text-sm font-body font-medium text-secondary/80 hover:text-primary border border-gold/15 hover:border-gold/40 bg-parchment/50 backdrop-blur-sm transition-all duration-200"
            >
              <BookOpen size={14} />
              Browse Library
            </Link>
            <Link
              to="/generate"
              className="flex items-center gap-1.5 px-4 py-2 rounded-md text-sm font-body font-medium text-primary-foreground bg-primary hover:bg-primary/90 transition-colors duration-200"
            >
              <Feather size={14} />
              Generate Blog
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Featured */}
      <section className="max-w-6xl mx-auto px-4 py-16 sm:py-20">
        <div className="flex items-center justify-between mb-10">
          <div>
            <h2 className="text-2xl sm:text-3xl font-heading font-semibold text-secondary">
              Recent Writings
            </h2>
            <p className="text-sm text-muted-foreground font-body mt-1">
              Latest entries from the archive
            </p>
          </div>
          {blogs && blogs.length > 6 && (
            <Link
              to="/library"
              className="hidden sm:flex items-center gap-1 text-sm font-body text-primary hover:underline"
            >
              View all <ArrowRight size={14} />
            </Link>
          )}
        </div>

        {isLoading && <Loader text="Retrieving archives…" />}

        {isError && (
          <div className="scroll-container p-10 text-center">
            <BookOpen size={32} className="mx-auto text-muted-foreground/40 mb-3" />
            <p className="text-sm text-muted-foreground font-body">
              Connect to the backend at <code className="text-xs bg-secondary/10 px-1.5 py-0.5 rounded">localhost:8000</code> to view blogs.
            </p>
          </div>
        )}

        {featured && featured.length > 0 && (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {featured.map((blog, i) => (
              <BlogCard
                key={blog.id}
                id={blog.id}
                title={blog.title}
                preview={blog.preview}
                tags={blog.tags}
                date={new Date(blog.created_at).toLocaleDateString()}
                index={i}
              />
            ))}
          </div>
        )}

        {featured && featured.length === 0 && !isLoading && (
          <div className="scroll-container p-12 text-center">
            <Feather size={32} className="mx-auto text-muted-foreground/40 mb-3" />
            <p className="text-sm text-muted-foreground font-body mb-4">
              No writings have been inscribed yet.
            </p>
            <Link
              to="/generate"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-sm font-body font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              <Feather size={14} />
              Create Your First Blog
            </Link>
          </div>
        )}
      </section>
    </PageLayout>
  );
};

export default Home;
