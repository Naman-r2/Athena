import { Search } from "lucide-react";
import { useState, FormEvent } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  initialValue?: string;
  size?: "default" | "large";
}

const SearchBar = ({
  onSearch,
  placeholder = "Search the archives…",
  initialValue = "",
  size = "default",
}: SearchBarProps) => {
  const [query, setQuery] = useState(initialValue);
  const [focused, setFocused] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim()) onSearch(query.trim());
  };

  const isLarge = size === "large";

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-xl mx-auto">
      <div className={`relative group transition-all duration-300 ${focused ? "scale-[1.01]" : ""}`}>
        <div className={`absolute inset-0 rounded-lg bg-gradient-to-r from-gold/20 via-gold/10 to-gold/20 blur-md opacity-0 transition-opacity duration-300 ${focused ? "opacity-100" : "group-hover:opacity-60"}`} />
        <div className="relative flex items-center">
          <Search
            size={isLarge ? 20 : 17}
            className="absolute left-4 text-muted-foreground group-focus-within:text-primary transition-colors duration-200"
          />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder={placeholder}
            className={`w-full ${isLarge ? "pl-12 pr-28 py-4 text-base" : "pl-11 pr-24 py-3 text-sm"} rounded-lg bg-parchment/90 backdrop-blur-sm border border-gold/20 font-body text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/20 transition-all duration-200`}
          />
          <button
            type="submit"
            className={`absolute right-2 ${isLarge ? "px-5 py-2" : "px-4 py-1.5"} rounded-md bg-primary text-primary-foreground font-body font-medium text-sm hover:bg-primary/90 transition-colors duration-200 active:scale-95`}
          >
            Search
          </button>
        </div>
      </div>
    </form>
  );
};

export default SearchBar;
