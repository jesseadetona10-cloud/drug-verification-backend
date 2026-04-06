with open('apps/drugs/views.py', 'r') as f:
    content = f.read()

approval_view = '''

class ApproveDrugView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        if request.user.role != "regulator":
            return Response({"detail": "Only regulators can approve drugs."}, status=status.HTTP_403_FORBIDDEN)
        try:
            drug = Drug.objects.get(pk=pk)
            drug.status = "active"
            drug.save()
            return Response({"detail": "Drug approved successfully."})
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)

class RejectDrugView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        if request.user.role != "regulator":
            return Response({"detail": "Only regulators can reject drugs."}, status=status.HTTP_403_FORBIDDEN)
        try:
            drug = Drug.objects.get(pk=pk)
            drug.status = "rejected"
            drug.save()
            return Response({"detail": "Drug rejected."})
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)

class PendingDrugsView(generics.ListAPIView):
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.role != "regulator":
            return Drug.objects.none()
        return Drug.objects.filter(status="pending")
'''

content = content + approval_view
with open('apps/drugs/views.py', 'w') as f:
    f.write(content)
print('Done')
