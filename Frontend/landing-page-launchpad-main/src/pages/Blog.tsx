import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { fetchBlogPosts, BlogPost } from "@/services/api";

const Blog = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPosts = async () => {
      setLoading(true);
      const data = await fetchBlogPosts();
      setPosts(data);
      setLoading(false);
    };
    loadPosts();
  }, []);

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

          {loading ? (
            <div className="text-center py-20 text-gray-500">Loading posts...</div>
          ) : filtered.length > 0 ? (
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
                      src={post.featured_image_url || "/placeholder.svg"}
                      alt={post.title}
                      className="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500"
                    />
                  </div>
                  <div className="p-6">
                    <div className="mb-2">
                       <span className="text-xs font-bold text-[#F4B400] uppercase tracking-wider">{post.category_name}</span>
                    </div>
                    <h2 className="text-xl font-semibold text-[#1F2E4D] mb-4">
                      {post.title}
                    </h2>
                    <p className="text-gray-600 mb-6">{post.excerpt}</p>
                    <Link
                      to={`/blog/${post.slug}`}
                      className="text-[#F4B400] font-bold hover:underline"
                    >
                      Read more →
                    </Link>
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center py-20 text-gray-500">No posts found.</div>
          )}
        </section>
      </main>

      <Footer />
    </>
  );
};

export default Blog;
