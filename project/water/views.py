from rest_framework import generics, permissions
from .models import WaterIntake
from .serializers import WaterIntakeSerializer
from datetime import date

    
class WaterIntakeView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterIntake.objects.all()
    serializer_class = WaterIntakeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WaterIntake.objects.filter(user=self.request.user, date=date.today())


    def perform_create(self, serializer):
        water_drunk = float(self.request.data.get('intake')) # assuming the frontend sends the amount of water as a float in the 'intake' field
        daily_goal = self.request.user.calculate_daily_water_goal()
        current_intake = sum([w.intake for w in self.request.user.waterintake_set.all()])

        if current_intake + water_drunk > daily_goal:
            # Handle the case where the user drinks more than their daily goal
            serializer.save(user=self.request.user, intake=daily_goal-current_intake)
        else:
            serializer.save(user=self.request.user)

        # Add the amount of water the user drank to their current intake
        current_intake += water_drunk
        self.request.user.update_current_water_intake(current_intake)

