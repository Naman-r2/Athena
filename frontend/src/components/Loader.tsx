import { motion } from "framer-motion";

const Loader = ({ text = "Loading…" }: { text?: string }) => (
  <div className="flex flex-col items-center justify-center py-20 gap-5">
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
      className="w-10 h-10 border-2 border-gold/20 border-t-gold rounded-full"
    />
    <p className="text-sm text-muted-foreground font-body animate-pulse">{text}</p>
  </div>
);

export default Loader;
