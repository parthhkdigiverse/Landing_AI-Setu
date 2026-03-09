import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Calendar, User, Clock, ArrowLeft } from "lucide-react";
import Blog1 from "@/assets/blog1.jpeg";
import Blog2 from "@/assets/blog2.jpg";
import Blog3 from "@/assets/blog3.png";
import Blog4 from "@/assets/blog4.jpg";
import Blog5 from "@/assets/blog5.jpg";
import Blog6 from "@/assets/blog6.png";

// replicate posts array or import from Blog page
const posts = [
  {
    id: 1,
    title: "How AI is Transforming Retail",
    author: "AI-Setu Team",
    date: "March 5, 2026",
    content:
      "Artificial intelligence is revolutionizing retail by enabling smarter inventory forecasts, personalized experiences, and efficient operations. Small retailers can now leverage predictive analytics to stay ahead of demand and optimize stock levels.\n\nWith AI-powered tools, shopkeepers can identify buying patterns and predict seasonal trends accurately. This not only reduces waste from overstocking but also prevents revenue loss from stockouts. Machine learning algorithms analyze historical data to recommend optimal reorder quantities and timings.\n\nPersonalization is another game-changer. AI enables retailers to understand customer preferences and build loyalty through targeted offers. From recommendation engines to dynamic pricing, AI tools help retailers compete with large chains.\n\nThe implementation is simpler than ever. Cloud-based AI solutions like AI-Setu require minimal technical expertise, making advanced technology accessible to small businesses across India.",
    image: Blog1,
  },
  {
    id: 2,
    title: "5 Tips to Boost Your Store’s Efficiency",    author: "Retail Solutions Expert",
    date: "March 7, 2026",    content:
      "Adopting mobile billing is the first step toward modernization. It saves time during checkout, enables bill generation anywhere in your shop, and provides instant sales records accessible from your phone.\n\nAutomating reporting eliminates manual spreadsheets and reduces errors. Daily, weekly, and monthly reports are generated automatically, helping you track performance and identify issues quickly.\n\nTraining your staff on POS usage is crucial. Well-trained employees reduce billing errors, process transactions faster, and provide better customer service. Invest in quick training sessions regularly.\n\nMaintaining accurate inventory is non-negotiable. Use barcoding or simple tracking tools to monitor stock in real-time. Regular physical counts help identify discrepancies early.\n\nFinally, review sales data weekly. Understanding which products sell best, which are slow movers, and seasonal patterns helps you make informed purchasing decisions and optimize your store layout.",
    image: Blog2,
  },
  {
    id: 3,
    title: "Why Cloud ERP Matters for SMEs",
    author: "Cloud Technology Lead",
    date: "March 6, 2026",
    content:
      "Cloud ERP solutions provide scalability, cost savings, and remote access. Unlike traditional on-premise systems requiring heavy upfront investment and dedicated IT staff, cloud ERP grows with your business.\n\nFor SMEs, moving to the cloud removes hardware maintenance overhead and offers real-time insights into operations. You access your business data anytime, anywhere, enabling better decision-making on the go.\n\nSecurity is built-in. Cloud providers invest heavily in data protection, ensuring your business information is safer than on local servers. Automatic backups mean you never lose critical data.\n\nCost-effectiveness is significant. Pay only for what you use, with flexible pricing models. This eliminates the burden of expensive IT infrastructure and allows you to allocate resources toward growth and customer satisfaction instead.",
    image: Blog3,
  },
  {
    id: 4,
    title: "AI-Setu Success Story: A Kirana Shop’s Growth",    author: "Customer Success Team",
    date: "March 8, 2026",    content:
      "One kirana shop in Delhi implemented AI-Setu ERP and saw remarkable results within four months. The owner, Rajesh Kumar, reported a 50% reduction in billing time through automated checkout and inventory management.\n\nRevenue increased by 30% because the system's smart reorder suggestions prevented stockouts of popular items. The AI learned from sales patterns and automatically suggested purchasing decisions, eliminating guesswork.\n\nOperational errors dropped significantly. With automated GST calculations and invoice generation, compliance became effortless. The staff required minimal training as the interface was intuitive and user-friendly.\n\nMost importantly, Rajesh could now manage his shop remotely. Mobile alerts notified him of low-stock items and daily sales summaries. This gave him peace of mind and more time for family, proving that technology truly empowers small business owners.",
    image: Blog4,
  },
  {
    id: 5,
    title: "Going Mobile with AI-Setu ERP",
    author: "Mobile Solutions Team",
    date: "March 4, 2026",
    content:
      "Managing your shop remotely is no longer a luxury—it's a necessity. AI-Setu's mobile dashboard transforms your smartphone into a powerful business command center. Check sales, inventory, and profit margins in real-time from anywhere.\n\nWhatsApp integration brings management to your fingertips. Receive instant alerts about low inventory, daily sales summaries, and customer orders through WhatsApp. No need to open an app; information comes directly to your messaging platform.\n\nGenerate invoices on the spot using your phone. Customers appreciate quick billing, and you gain instant payment confirmation. The mobile app works offline too—sync when you're connected to internet.\n\nThis flexibility enables you to attend to customer needs, visit suppliers, or handle emergencies without losing control of your business. Modern retailers know that being tethered to a desk is outdated. Embrace mobility and watch your business grow.",
    image: Blog5,
  },
  {
    id: 6,
    title: "Top 5 Features of AI-Setu ERP You Shouldn’t Miss",    author: "Product Team",
    date: "March 3, 2026",    content:
      "Smart Reorder Suggestions is a game-changer. The AI learns your sales patterns and automatically suggests when to reorder which products in what quantities. This prevents both overstocking and stockouts, maximizing profit margins.\n\nGST-Compliant Invoicing ensures you're always audit-ready. Automatic tax calculations, compliance reports, and invoice generation reduce errors and save countless hours on paperwork.\n\nReal-Time Sales Analytics provide insights into your business performance. Understand which products are bestsellers, identify trends, and make data-driven decisions instead of relying on intuition.\n\nWhatsApp and Mobile Integration keeps you connected. Get alerts about stockouts, high-value sales, and daily summaries on your phone. Manage your entire business from your pocket.\n\nInventory Management with Barcode Support streamlines stock tracking. Reduce human errors, prevent theft, and maintain accurate records automatically. The system tracks expiry dates too, ensuring product quality and compliance.",
    image: Blog6,
  },
];

const BlogPost = () => {
  const { postId } = useParams<{ postId: string }>();
  const post = posts.find((p) => p.id === Number(postId));

  if (!post) {
    return (
      <>
        <Header />
        <main className="min-h-[60vh] flex items-center justify-center bg-gradient-to-br from-[#F5F6FA] to-[#E8ECF4]">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="text-center bg-white/90 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-white/20"
          >
            <h1 className="text-3xl font-bold text-[#1F2E4D] mb-4">Post not found</h1>
            <Link to="/blog" className="inline-flex items-center gap-2 text-[#F4B400] font-semibold hover:text-[#E6B800] transition-colors duration-300">
              <ArrowLeft size={20} />
              Back to blog
            </Link>
          </motion.div>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="bg-gradient-to-br from-[#F5F6FA] via-[#F0F2F9] to-[#E8ECF4] min-h-screen overflow-x-hidden">
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="max-w-6xl mx-auto px-6 py-16"
        >
          {/* Breadcrumb */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{
              delay: 0.2,
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="mb-8"
          >
            <Link to="/blog" className="inline-flex items-center gap-2 text-[#F4B400] hover:text-[#E6B800] transition-colors duration-300 font-medium">
              <ArrowLeft size={18} />
              Back to Blog
            </Link>
          </motion.div>

          {/* Title */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.3,
              duration: 0.6,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="text-5xl md:text-6xl font-bold text-[#1F2E4D] mb-6 leading-tight"
          >
            {post.title}
          </motion.h1>

          {/* Meta Information */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.4,
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="flex flex-wrap items-center gap-6 mb-8 p-6 bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20"
          >
            <div className="flex items-center gap-2 text-gray-700">
              <User size={18} className="text-[#F4B400]" />
              <span className="font-medium">{post.author}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <Calendar size={18} className="text-[#F4B400]" />
              <span>{post.date}</span>
            </div>
          </motion.div>

          {/* Featured Image and Content Container */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.5,
              duration: 0.6,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
          >
            {/* Featured Image */}
            <div className="relative overflow-hidden rounded-t-3xl shadow-2xl group mb-0">
              <img
                src={post.image}
                alt={post.title}
                className="w-full h-auto max-h-[500px] object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent group-hover:from-black/30 transition-all duration-500"></div>
            </div>

            {/* Content */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: 0.6,
                duration: 0.5,
                ease: [0.25, 0.46, 0.45, 0.94]
              }}
              className="prose prose-xl max-w-none bg-white/90 backdrop-blur-sm p-8 md:p-12 rounded-b-3xl shadow-2xl border border-white/30 border-t-0 relative z-10"
            >
              {post.content.split('\n\n').map((paragraph, idx) => (
              <motion.p
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  delay: 0.8 + idx * 0.1,
                  duration: 0.5,
                  ease: [0.25, 0.46, 0.45, 0.94]
                }}
                className="text-gray-800 leading-relaxed mb-6 text-lg font-medium"
              >
                {paragraph}
              </motion.p>
            ))}
            </motion.div>
          </motion.div>

          {/* Bottom Navigation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 1.0,
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="mt-16 text-center"
          >
            <Link
              to="/blog"
              className="inline-flex items-center gap-3 bg-gradient-to-r from-[#F4B400] to-[#E6B800] text-white px-8 py-4 rounded-full font-bold hover:from-[#E6B800] hover:to-[#D4A600] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <ArrowLeft size={20} />
              Back to All Articles
            </Link>
          </motion.div>
        </motion.section>
      </main>
      <Footer />
    </>
  );
};

export default BlogPost;
