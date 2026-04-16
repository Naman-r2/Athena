import GreekDivider from "./GreekDivider";

const Footer = () => (
  <footer className="mt-auto pt-12 pb-8">
    <div className="max-w-6xl mx-auto px-4">
      <GreekDivider className="mb-8" />
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <p className="text-sm text-muted-foreground font-heading tracking-wider">
          Athena — Knowledge Engine
        </p>
        <p className="text-xs text-muted-foreground/60 font-body">
          AI-Powered Technical Blog Platform
        </p>
      </div>
    </div>
  </footer>
);

export default Footer;
