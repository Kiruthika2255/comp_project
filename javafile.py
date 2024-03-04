import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@SpringBootApplication
@RestController
public class TrainTicketApplication {

    private final Map<String, TrainSection> trainData = new HashMap<>();

    public static void main(String[] args) {
        SpringApplication.run(TrainTicketApplication.class, args);
    }

    // API to submit a purchase for a ticket
    @PostMapping("/purchase")
    public Map<String, String> purchaseTicket(@RequestBody PurchaseRequest request) {
        String section = allocateSeat();
        TrainSection trainSection = trainData.computeIfAbsent(section, k -> new TrainSection());
        String seat = trainSection.allocateSeat();
        trainSection.addUser(request, seat);
        Map<String, String> response = new HashMap<>();
        response.put("message", "Purchase successful");
        response.put("seat_allocation", seat);
        return response;
    }

    // API to show the details of the receipt for the user
    @GetMapping("/receipt/{user}")
    public Object getReceipt(@PathVariable String user) {
        for (TrainSection section : trainData.values()) {
            User userDetails = section.getUserDetails(user);
            if (userDetails != null) {
                return userDetails;
            }
        }
        Map<String, String> error = new HashMap<>();
        error.put("error", "User not found");
        return error;
    }

    // API to view users and seat allocation by section
    @GetMapping("/view/{section}")
    public Object viewUsersBySection(@PathVariable String section) {
        TrainSection trainSection = trainData.get(section);
        if (trainSection != null) {
            return trainSection.getUsers();
        }
        Map<String, String> error = new HashMap<>();
        error.put("error", "Invalid section");
        return error;
    }

    // API to remove a user from the train
    @DeleteMapping("/remove/{user}")
    public Map<String, String> removeUser(@PathVariable String user) {
        for (TrainSection section : trainData.values()) {
            if (section.removeUser(user)) {
                Map<String, String> response = new HashMap<>();
                response.put("message", "User removed successfully");
                return response;
            }
        }
        Map<String, String> error = new HashMap<>();
        error.put("error", "User not found");
        return error;
    }

    // API to modify a user's seat
    @PutMapping("/modify/{user}/{newSeat}")
    public Map<String, String> modifySeat(@PathVariable String user, @PathVariable String newSeat) {
        for (TrainSection section : trainData.values()) {
            if (section.modifySeat(user, newSeat)) {
                Map<String, String> response = new HashMap<>();
                response.put("message", "Seat modified successfully");
                response.put("new_seat", newSeat);
                return response;
            }
        }
        Map<String, String> error = new HashMap<>();
        error.put("error", "User not found");
        return error;
    }

    // Helper method to allocate a seat in a section
    private String allocateSeat() {
        for (String section : trainData.keySet()) {
            TrainSection trainSection = trainData.get(section);
            if (trainSection.getNumberOfUsers() < 2) {
                return section;
            }
        }
        return null; // No available seats
    }
}

class TrainSection {
    private int seatCounter = 0;
    private Map<String, User> users = new HashMap<>();

    String allocateSeat() {
        seatCounter++;
        return "Seat" + seatCounter;
    }

    void addUser(PurchaseRequest request, String seat) {
        users.put(request.getUser().getEmail(), new User(request, seat));
    }

    User getUserDetails(String userEmail) {
        return users.get(userEmail);
    }

    Map<String, User> getUsers() {
        return users;
    }

    boolean removeUser(String userEmail) {
        return users.remove(userEmail) != null;
    }

    boolean modifySeat(String userEmail, String newSeat) {
        User user = users.get(userEmail);
        if (user != null) {
            user.setSeat(newSeat);
            return true;
        }
        return false;
    }

    int getNumberOfUsers() {
        return users.size();
    }
}

class User {
    private String firstName;
    private String lastName;
    private String email;
    private String from;
    private String to;
    private int pricePaid;
    private String seat;

    public User(PurchaseRequest request, String seat) {
        this.firstName = request.getUser().getFirstName();
        this.lastName = request.getUser().getLastName();
        this.email = request.getUser().getEmail();
        this.from = request.getFrom();
        this.to = request.getTo();
        this.pricePaid = 5;
        this.seat = seat;
    }

    // Getters and setters
}

class PurchaseRequest {
    private String from;
    private String to;
    private UserDetails user;

    // Getters and setters

}

class UserDetails {
    private String firstName;
    private String lastName;
    private String email;

    // Getters and setters
}
