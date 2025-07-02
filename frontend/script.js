async function fetchFlights() {
  try {
    const res = await fetch("http://localhost:5000/api/flights");
    const flights = await res.json();

    const tbody = document.querySelector("#flightTable tbody");
    tbody.innerHTML = "";

    flights.forEach(flight => {
      const row = document.createElement("tr");

      // Highlight landed flights
      if (flight.Status && flight.Status.toLowerCase() === "landed") {
        row.classList.add("landed");
      }

      row.innerHTML = `
        <td>${flight.Name}</td>
        <td>${flight.Phone}</td>
        <td>${new Date(flight.Date).toLocaleDateString()}</td>
        <td>${flight.Time}</td>
        <td>${flight.Airline}</td>
        <td>${flight.FlightNumber}</td>
        <td>${flight.PassengerCount}</td>
        <td>${flight.ArrivalAirport}</td>
        <td class="status">${flight.Status || "Unknown"}</td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching flights:", err);
  }
}

// Fetch flights on page load and refresh every 5 minutes
fetchFlights();
setInterval(fetchFlights, 5 * 60 * 1000);
