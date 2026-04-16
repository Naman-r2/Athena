import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { BookOpen } from "lucide-react";
import PageLayout from "@/components/PageLayout";
import BlogCard from "@/components/BlogCard";
import SearchBar from "@/components/SearchBar";
import Loader from "@/components/Loader";
import ErrorMessage from "@/components/ErrorMessage";
import GreekDivider from "@/components/GreekDivider";
import { fetchBlogs, searchBlogs } from "@/lib/api";
import { useState } from "react";

const Library = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  const { data: blogs, isLoading, isError, refetch } = useQuery({
    queryKey: ["blogs"],
    queryFn: fetchBlogs,
    retry: 1,
  });

  const { data: searchResults, isLoading: isSearchLoading } = useQuery({
    queryKey: ["search", searchQuery],
    queryFn: () => searchBlogs(searchQuery),
    enabled: !!searchQuery,
    retry: 1,
  });

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setIsSearching(!!query);
  };

  const displayedBlogs = isSearching ? (searchResults || []) : (blogs || []);

  return (
    <PageLayout>
      <div className="max-w-6xl mx-auto px-4 py-12 sm:py-16">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-10"
        >
          <h1 className="text-3xl sm:text-4xl font-heading font-bold text-secondary mb-1">
            The Archive
          </h1>
          <p className="text-sm text-muted-foreground font-body">
            All writings preserved in the library
          </p>
          <GreekDivider className="mt-5" />
        </motion.div>

        {/* Search Bar */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="mb-8"
        >
          <SearchBar onSearch={handleSearch} />
        </motion.div>

        {isSearching && searchQuery && (
          <p className="text-xs text-muted-foreground/60 font-body mb-2">
            Search results for "{searchQuery}"
          </p>
        )}

        {(isLoading || isSearchLoading) && <Loader text={isSearching ? "Searching archives…" : "Loading archives…"} />}
        {isError && <ErrorMessage message="Could not reach the archive." onRetry={() => refetch()} />}

        {displayedBlogs && displayedBlogs.length > 0 && (
          <>
            {!isSearching && (
              <p className="text-xs text-muted-foreground/60 font-body mb-5">
                {displayedBlogs.length} {displayedBlogs.length === 1 ? "entry" : "entries"} found
              </p>
            )}
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {displayedBlogs.map((blog, i) => (
                <BlogCard
                  key={blog.id}
                  id={blog.id}
                  title={blog.title}
                  preview={blog.preview}
                  tags={blog.tags}
                  imageUrl={blog.image_url}
                  date={new Date(blog.created_at).toLocaleDateString()}
                  index={i}
                />
              ))}
            </div>
          </>
        )}

        {displayedBlogs && displayedBlogs.length === 0 && (
          <div className="scroll-container p-16 text-center">
            <BookOpen size={36} className="mx-auto text-muted-foreground/30 mb-4" />
            <p className="text-sm text-muted-foreground font-body">
              {isSearching ? `No results found for "${searchQuery}"` : "The archive awaits its first inscription."}
            </p>
          </div>
        )}
      </div>
    </PageLayout>
  );
};

export default Library;
