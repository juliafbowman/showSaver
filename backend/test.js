// Test POST /api/rating
async function test() {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/db/import?id=355772&type=movie",
      {
        method: "GET",
      }
    );

    const data = await response.json();
    console.log("Status:", response.status);
    console.log("Response:", data);

    if (response.ok) {
      console.log("✓");
    } else {
      console.log("✗ Error:", data.error);
    }
  } catch (error) {
    console.error("Network error:", error);
  }
}

// Run the test
test();
