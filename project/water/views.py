from rest_framework import generics, permissions
from .models import WaterIntake
from .serializers import WaterIntakeSerializer
 
class WaterIntakeView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterIntake.objects.all()
    serializer_class = WaterIntakeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WaterIntake.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
