import Header from "@/components/Header";
import Footer from "@/components/Footer";

const ComingSoon = ({ title }: { title: string }) => (
  <>
    <Header />
    <main className="min-h-[60vh] flex items-center justify-center bg-background">
      <div className="text-center">
        <h1 className="font-heading font-bold text-4xl text-foreground mb-3">{title}</h1>
        <p className="text-muted-foreground">This page is coming soon. Stay tuned!</p>
      </div>
    </main>
    <Footer />
  </>
);

export const About = () => <ComingSoon title="About Us" />;
export const Blog = () => <ComingSoon title="Blog" />;
export const Career = () => <ComingSoon title="Career" />;
export const Contact = () => <ComingSoon title="Contact Us" />;
