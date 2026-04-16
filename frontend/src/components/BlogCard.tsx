import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Calendar } from "lucide-react";

interface BlogCardProps {
  id: string;
  title: string;
  preview: string;
  tags: string[];
  date: string;
  imageUrl?: string;
  index?: number;
}

const BlogCard = ({ id, title, preview, tags, date, imageUrl, index = 0 }: BlogCardProps) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.4, delay: index * 0.08 }}
  >
    <Link
      to={`/blog/${id}`}
      className="group relative block rounded overflow-hidden bg-parchment border border-gold/15 hover:border-gold/40 transition-all duration-300 hover:shadow-[0_8px_30px_-8px_hsl(43_72%_47%/0.15)]"
    >
      {/* Image */}
      {imageUrl && (
        <div className="aspect-video overflow-hidden">
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        </div>
      )}
      
      {/* Gold accent top bar */}
      <div className="h-1 bg-gradient-to-r from-gold/40 via-gold/80 to-gold/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="p-6">
        <h3 className="font-heading text-lg font-semibold text-secondary group-hover:text-primary transition-colors duration-200 mb-2.5 line-clamp-2 leading-snug">
          {title}
        </h3>
        <p className="text-sm text-muted-foreground font-body line-clamp-3 mb-5 leading-relaxed">
          {preview}
        </p>
        
        <div className="flex items-end justify-between gap-3">
          <div className="flex flex-wrap gap-1.5">
            {tags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="text-[11px] font-body font-medium px-2.5 py-1 rounded-sm bg-secondary/8 text-secondary/80 border border-secondary/10"
              >
                {tag}
              </span>
            ))}
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <span className="flex items-center gap-1 text-[11px] text-muted-foreground/70 font-body">
              <Calendar size={11} />
              {date}
            </span>
            <ArrowRight size={14} className="text-muted-foreground/40 group-hover:text-primary group-hover:translate-x-0.5 transition-all duration-200" />
          </div>
        </div>
      </div>
    </Link>
  </motion.div>
);

export default BlogCard;
