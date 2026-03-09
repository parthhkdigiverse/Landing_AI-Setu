import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { useState } from "react";
import Blog1 from "@/assets/blog1.jpeg";
import Blog2 from "@/assets/blog2.jpg";
import Blog3 from "@/assets/blog3.png";
import Blog4 from "@/assets/blog4.jpg";
import Blog5 from "@/assets/blog5.jpg";
import Blog6 from "@/assets/blog6.png";

const posts = [
  {
    id: 1,
    title: "How AI is Transforming Retail",
    excerpt:
      "Discover how artificial intelligence is helping small retailers forecast demand, manage inventory, and personalize customer experiences.",
    image: Blog1,
  },
  {
    id: 2,
    title: "5 Tips to Boost Your Store’s Efficiency",
    excerpt:
      "Simple operational changes that can make a big difference in how your shop runs, from mobile billing to automated reports.",
    image: Blog2,
  },
  {
    id: 3,
    title: "Why Cloud ERP Matters for SMEs",
    excerpt:
      "Learn why migrating your business systems to the cloud is a game‑changer for scalability and cost control.",
    image: Blog3,
  },
  {
    id: 4,
    title: "AI-Setu Success Story: A Kirana Shop’s Growth",
    excerpt:
      "Read how one small kirana store cut billing times in half and increased monthly revenue by adopting AI-Setu ERP.",
    image: Blog4,
  },
  {
    id: 5,
    title: "Going Mobile with AI-Setu ERP",
    excerpt:
      "Explore the benefits of managing your store on the go using AI-Setu’s mobile dashboard and WhatsApp integrations.",
    image: Blog5,
  },
  {
    id: 6,
    title: "Top 5 Features of AI-Setu ERP You Shouldn’t Miss",
    excerpt:
      "From smart reorder suggestions to GST-compliant invoicing, discover the features that make AI-Setu ERP a must-have for retailers.",
    image: Blog6,
  },
];

const Blog = () => {
  const [search, setSearch] = useState("");
  const filtered = posts.filter(
    (p) =>
      p.title.toLowerCase().includes(search.toLowerCase()) ||
      p.excerpt.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <Header />

      <main className="bg-[#F5F6FA] py-24">
        <section className="max-w-6xl mx-auto px-6">
          {/* search bar */}
          <div className="mb-12 text-center">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search articles..."
              className="w-full md:w-1/2 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1F2E4D]"
            />
          </div>
          <motion.h1
            initial={{ opacity: 0, y: -40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="text-5xl font-bold text-[#1F2E4D] mb-12 text-center"
          >
            Our Blog
          </motion.h1>

          <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-3">
            {filtered.map((post, idx) => (
              <motion.div
                key={post.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.2, duration: 0.6, ease: "easeOut" }}
                className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-shadow duration-300"
              >
                <div className="h-48 overflow-hidden">
                  <img
                    src={post.image}
                    alt={post.title}
                    className="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500"
                  />
                </div>
                <div className="p-6">
                  <h2 className="text-xl font-semibold text-[#1F2E4D] mb-4">
                    {post.title}
                  </h2>
                  <p className="text-gray-600 mb-6">{post.excerpt}</p>
                  <Link
                    to={`/blog/${post.id}`}
                    className="text-[#F4B400] font-bold hover:underline"
                  >
                    Read more →
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
};

export default Blog;
