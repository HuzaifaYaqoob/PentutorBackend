

from unicodedata import category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChapterVideoSerializer, CourseCategorySerializer, CourseChapterSerializer, CourseMediaSerializer, CourseSerializer, CourseReviewSerializer, CartItemSerializer

from .models import CartItem, ChapterVideo, Course, CourseCategory, CourseChapter, CourseMedia, CourseReview

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_courses(request):
    all_courses = Course.objects.all()
    serialized = CourseSerializer(all_courses, many=True)

    return Response(
        {
            'status' : True,
            'data' : serialized.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    title = request.data['title'] if 'title' in request.data else None
    language = request.data['language'] if 'language' in request.data else None
    course_category = request.data['course_category'] if 'course_category' in request.data else None
    level = request.data['level'] if 'level' in request.data else None
    price = request.data['price'] if 'price' in request.data else None
    description = request.data['description'] if 'description' in request.data else None
    image = request.data['image'] if 'image' in request.data else None
    try:
        user = request.user
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if not title or not language or not course_category or not level or not price or not description or not image:
        
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.data._mutable = True
    request.data['user'] = user.id
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        course = serializer.save()
        course_media = CourseMedia.objects.create(course=course, image=image)
        return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status' : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_course(request):
    slug = request.data['slug'] if 'slug' in request.data else None
    if not slug:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = request.user
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        course = Course.objects.get(slug=slug)
        if user == course.user:
            course.delete()
            return Response({'status' : True, 'data' : 'Course Deleted Succesfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status' : False, 'data' : 'You have no permission to deleted course!'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_course(request):
    slug = request.data['slug'] if 'slug' in request.data else None
    title = request.data['title'] if 'title' in request.data else None
    language = request.data['language'] if 'language' in request.data else None
    category = request.data['category'] if 'category' in request.data else None
    level = request.data['level'] if 'level' in request.data else None
    price = request.data['price'] if 'price' in request.data else None
    description = request.data['description'] if 'description' in request.data else None
    try:
        user = request.user
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if not slug:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        course = Course.objects.get(slug=slug)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if title:
        course.title = title
    if language:
        course.language = language
    if category:
        course.category = category
    if level:
        course.level = level
    if price:
        course.price = price
        
    if description:
        course.description = description
    course.save()
    serializer = CourseSerializer(course)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course_media(request):
    course = request.data['course'] if 'course' in request.data else None
    image = request.data['image'] if 'image' in request.data else None

    if not course:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    media = CourseMedia.objects.create(course=course, image=image)
    serializer = CourseMediaSerializer(media)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)

    
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_category(request):
    category = CourseCategory.objects.all()
    serializer = CourseCategorySerializer(category, many=True)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course_chapter(request):
    course = request.data['course'] if 'course' in request.data else None
    title = request.data['title'] if 'title' in request.data else None
    if not course or not title:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CourseChapterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status' : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chapter_video(request):
    chapter = request.data['chapter'] if 'chapter' in request.data else None
    video = request.data['video'] if 'video' in request.data else None
    title = request.data['title'] if 'title' in request.data else None
    
    if not chapter or not video or not title:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        chapter = CourseChapter.objects.get(slug=chapter)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    video = ChapterVideo.objects.create(video=video, chapter=chapter, course=chapter.course, title=title)
    serializer = ChapterVideoSerializer(video)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chapter_video(request):
    user = request.user
    video = request.data['video'] if 'video' in request.data else None
    if not video:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        video = ChapterVideo.objects.get(slug=video)
    except Exception as e:
        return Response({'status' : False, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    if user == video.chapter.course.user:
        video.delete()
        return Response({'status' : True, 'data' : 'Video Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'status' : False, 'data' : 'Ops, You have no permission to delete video!'}, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_courses(request):
    user = request.user
    courses = Course.objects.filter(user=user)
    serializer = CourseSerializer(courses, many=True)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_course_chapter(request):
    title = request.data['title'] if 'title' in request.data else None
    chapter = request.data['chapter'] if 'chapter' in request.data else None
    
    if not chapter:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        chapter = CourseChapter.objects.get(slug=chapter)
    except Exception as e:
        return Response({'status' : True, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    if title:
        chapter.title = title
    chapter.save()
    serializer = CourseChapterSerializer(chapter)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_course_chapters(request):
    course = request.query_params.get('course', None)
    if not course:
        return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'status' : True, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    chapters = CourseChapter.objects.filter(course=course)
    serializer = CourseChapterSerializer(chapters, many=True)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_course(request):
    course = request.query_params.get('course', None)
    if not course:
            return Response({'status' : False, 'data' : 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'status' : True, 'data' : str(e)}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course)
    return Response({'status' : True, 'data' : serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_store_rating(request):
    course = request.data['course'] if 'course' in request.data else None
    review = request.data['review'] if 'review' in request.data else None
    rate = request.data['rate'] if 'rate' in request.data else None
    user = request.user
    
    if not course or not review or not rate:
        return Response({"success": False, 'response': 'Invalid Data!'},
                    status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)

    rating = CourseReview.objects.create(course=course, review=review, rate=rate, user=user)
    serializer = CourseReviewSerializer(rating)
    return Response({'success': True, 'message': serializer.data},
                                status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_store_rating(request):
    course = request.query_params.get('business_store', None)
    if not course:
        return Response({"success": False, 'response': 'Invalid Data!'},
                    status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)

    rating = CourseReview.objects.filter(course=course)

    serializer = CourseReviewSerializer(rating, many=True)
    return Response({'success': True, 'message': serializer.data},
                                status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_store_rating(request):
    rating = request.data['rating'] if 'rating' in request.data else None

    if not rating:
        return Response({"success": False, 'response': 'Invalid Data!'},
                    status=status.HTTP_400_BAD_REQUEST)
    try:
        rating = CourseReview.objects.get(slug=rating)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    
    rating.delete()
    return Response({'success': True, 'message': 'Deleted Successfully!'},
                                status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_store_rating(request):
    rating = request.data['rating'] if 'rating' in request.data else None
    review = request.data['review'] if 'review' in request.data else None
    rate = request.data['rate'] if 'rate' in request.data else None
    user = request.user

    try:
        rating = CourseReview.objects.get(slug=rating)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    if review:
        rating.review = review
    if rate:
        rating.rate = rate
    rating.save()

    serializer = CourseReviewSerializer(rating)
    return Response({'success': True, 'message': serializer.data},
                                status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    course = request.data['course'] if 'course' in request.data else None
    quantity = request.data['quantity'] if 'quantity' in request.data else None
    if not course:
        return Response({"success": False, 'response': 'Invalid Data!'},
                    status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(slug=course)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    if not quantity:
        quantity = 1 
    cart = CartItem.objects.create(course=course, user=user, quantity=quantity, course_cart=True)
    serializer = CartItemSerializer(cart)
    return Response({'success': True, 'message': serializer.data},
                                status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_cart(request):
    user = request.user
    cart = CartItem.objects.filter(user=user)
    serializer = CartItemSerializer(cart, many=True)
    return Response({'success': True, 'message': serializer.data},
                                status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    user = request.user
    cart = request.data['cart'] if 'cart' in request.data else None
    if not cart:
        return Response({"success": False, 'response': 'Invalid Data!'},
                    status=status.HTTP_400_BAD_REQUEST)
    try:
        cart = CartItem.objects.get(slug=cart)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    if user == cart.user:
        cart.delete()
        return Response({"success": True, 'response': 'Deleted Successfully!'},
                status=status.HTTP_200_OK)
    else:
        return Response({"success": False, 'response': 'Ops, You have no permission to delete!'},
            status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    user = request.user
    quantity = request.data['quantity'] if 'quantity' in request.data else None
    cart = request.data['cart'] if 'cart' in request.data else None
    if not cart:
        return Response({"success": False, 'response': 'Invalid Data!'},
                    status=status.HTTP_400_BAD_REQUEST)
    try:
        cart = CartItem.objects.get(slug=cart)
    except Exception as e:
        return Response({'success': False, 'response': str(e)},
                        status=status.HTTP_404_NOT_FOUND)
    if user == cart.user:
        if quantity:
            cart.quantity = quantity
            cart.save()
        serializer = CartItemSerializer(cart)
        return Response({"success": True, 'response': serializer.data},
                status=status.HTTP_200_OK)
    else:
        return Response({"success": False, 'response': 'Ops, You have no permission to update!'},
            status=status.HTTP_400_BAD_REQUEST)
        
        
    