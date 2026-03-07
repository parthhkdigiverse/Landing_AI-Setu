import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ContactUsPage from "@/components/ContactUs";
import CareerPage from "@/components/Career";


const ComingSoon = ({ title }: { title: string }) => {
  if (title === "Career") {
    return <CareerPage />;
  }


  if (title === "Contact") {
    return <ContactUsPage />;
  }

  return (
    <>
      <Header />

      <main className="min-h-[60vh] flex items-center justify-center bg-background">
        <div className="text-center">
          <h1 className="font-bold text-4xl mb-3">{title}</h1>
          <p className="text-gray-500">This page is coming soon. Stay tuned!</p>
        </div>
      </main>

      <Footer />
    </>
  );
};

export const About = () => <ComingSoon title="About Us" />;
export const Blog = () => <ComingSoon title="Blog" />;
export const Career = () => <ComingSoon title="Career" />;
export const Contact = () => <ComingSoon title="Contact" />;

export default ComingSoon;