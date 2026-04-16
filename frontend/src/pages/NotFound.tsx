import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import PageLayout from "@/components/PageLayout";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <PageLayout>
      <div className="flex flex-col items-center justify-center py-32 px-4 text-center">
        <p className="text-7xl font-heading font-bold text-primary/30 mb-4">404</p>
        <h1 className="text-2xl font-heading font-semibold text-secondary mb-2">
          Scroll Not Found
        </h1>
        <p className="text-sm text-muted-foreground font-body mb-8">
          This path does not lead to any known archive.
        </p>
        <Link
          to="/"
          className="px-5 py-2.5 rounded-md text-sm font-body font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
        >
          Return Home
        </Link>
      </div>
    </PageLayout>
  );
};

export default NotFound;
