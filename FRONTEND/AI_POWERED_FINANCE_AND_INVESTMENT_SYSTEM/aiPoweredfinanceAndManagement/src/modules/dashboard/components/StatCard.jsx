export default function StatCard({ title, value, color }) {
  const colors = {
    red: "bg-red-500",
    orange: "bg-orange-500",
    yellow: "bg-yellow-500",
    blue: "bg-blue-500",
  };

  return (
    <div className={`${colors[color]} text-white p-6 rounded-xl shadow-md`}>
      <h4 className="text-sm opacity-80">{title}</h4>
      <p className="text-2xl font-bold mt-2">{value}</p>
    </div>
  );
}