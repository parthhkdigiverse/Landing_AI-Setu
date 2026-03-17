import { useEffect, useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useParams } from "react-router-dom";

const PolicyPage = () => {
  const { slug } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/policies/${slug}/`)
      .then(res => res.json())
      .then(setData);
  }, [slug]);

  if (!data) return <div className="text-center py-20">Loading...</div>;

  return (
    <>
      <Header />

      <main>
        {/* HERO */}
        <div className="bg-[#1F2E4D] text-white py-16 text-center">
          <h1 className="text-4xl font-bold">{data.title}</h1>
        </div>

        {/* CONTENT */}
        <div className="max-w-3xl mx-auto py-12 px-6">

          {/* DESCRIPTION */}
          <p className="text-gray-600 mb-8">
            {data.description}
          </p>

          {/* SECTIONS */}
          <div className="space-y-6">
            {data.sections.map((sec: any) => (
              <div key={sec.id}>
                <h3 className="font-bold text-lg mb-2">
                  {sec.heading}
                </h3>
                <p className="text-gray-600">
                  {sec.content}
                </p>
              </div>
            ))}
          </div>

        </div>
      </main>

      <Footer />
    </>
  );
};

export default PolicyPage;