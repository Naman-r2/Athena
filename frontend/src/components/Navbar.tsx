import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import { Menu, X, BookOpen, Feather, Home, Lightbulb } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// Athena logo component
const AthenaLogo = () => (
  <svg
    viewBox="0 0 100 100"
    fill="currentColor"
    className="w-10 h-10 text-secondary group-hover:text-primary transition-colors duration-200"
    xmlns="http://www.w3.org/2000/svg"
  >
    {/* Helmet shape (Greek warrior helmet) */}
    <g>
      {/* Helmet dome */}
      <ellipse cx="50" cy="42" rx="30" ry="34" className="fill-current" />
      {/* Cheekpieces */}
      <rect x="16" y="36" width="9" height="22" rx="2" className="fill-current" />
      <rect x="75" y="36" width="9" height="22" rx="2" className="fill-current" />
      {/* Nose guard */}
      <polygon points="50,48 46,68 54,68" className="fill-current" />
      {/* Crest top */}
      <rect x="45" y="2" width="10" height="14" className="fill-primary opacity-90" />
      {/* Crest */}
      <polygon points="50,16 40,30 60,30" className="fill-primary opacity-90" />
    </g>
    {/* Eye openings */}
    <circle cx="38" cy="40" r="4" className="fill-parchment opacity-80" />
    <circle cx="62" cy="40" r="4" className="fill-parchment opacity-80" />
  </svg>
);

const navLinks = [
  { to: "/", label: "Home", icon: Home },
  { to: "/library", label: "Library", icon: BookOpen },
  { to: "/generate", label: "Generate", icon: Feather },
];

const Navbar = () => {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-xl bg-card/70 border-b border-gold/10">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-8">
          {/* Logo - flush left */}
          <Link to="/" className="flex items-center gap-3 group shrink-0">
            <AthenaLogo />
            <div className="flex flex-col leading-tight">
              <span className="text-lg font-heading font-bold text-secondary tracking-wide group-hover:text-primary transition-colors">
                Athena
              </span>
              <span className="text-[9px] text-muted-foreground font-body tracking-[0.15em] uppercase hidden sm:block">
                Oracle
              </span>
            </div>
          </Link>

          {/* Desktop nav - centered */}
          <div className="hidden md:flex items-center justify-center flex-1 gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`relative flex items-center gap-2 px-5 py-2.5 rounded text-sm font-body font-medium transition-all duration-200 ${
                    isActive
                      ? "text-primary bg-primary/5"
                      : "text-muted-foreground hover:text-primary hover:bg-primary/5"
                  }`}
                >
                  <Icon size={20} strokeWidth={isActive ? 2.2 : 1.8} />
                  {link.label}
                  {isActive && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="absolute bottom-0 left-2 right-2 h-0.5 bg-primary rounded-full"
                      transition={{ type: "spring", stiffness: 350, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>

          {/* Mobile toggle */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-muted-foreground hover:text-primary transition-colors"
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {/* Mobile menu */}
        <AnimatePresence>
          {mobileOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="md:hidden overflow-hidden"
            >
              <div className="pb-4 space-y-1 pt-1">
                {navLinks.map((link) => {
                  const Icon = link.icon;
                  return (
                    <Link
                      key={link.to}
                      to={link.to}
                      onClick={() => setMobileOpen(false)}
                      className={`flex items-center gap-3 px-4 py-3 rounded text-sm font-body transition-colors ${
                        location.pathname === link.to
                          ? "text-primary bg-primary/10"
                          : "text-muted-foreground hover:text-primary hover:bg-primary/5"
                      }`}
                    >
                      <Icon size={20} />
                      {link.label}
                    </Link>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  );
};

export default Navbar;
