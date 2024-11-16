import React, { useState } from 'react';
import {
  ChakraProvider,
  Box,
  VStack,
  Heading,
  Text,
  Input,
  Button,
  Image,
  useToast,
  Container,
  Progress,
} from '@chakra-ui/react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const toast = useToast();

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    },
    multiple: false,
  });

  const handleUpscale = async () => {
    if (!image) {
      toast({
        title: 'No image selected',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('image', image);
    formData.append('prompt', prompt);

    try {
      const response = await axios.post('http://localhost:8000/api/upscale', formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minute timeout
      });

      const url = URL.createObjectURL(response.data);
      setResult(url);
      toast({
        title: 'Image upscaled successfully!',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      console.error('Error details:', error);
      const errorMessage = error.response?.data?.error || error.message || 'Unknown error occurred';
      toast({
        title: 'Error upscaling image',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={10}>
        <VStack spacing={8}>
          <Heading>Image Upscaler</Heading>
          <Text>Transform your low-resolution images into high-quality masterpieces</Text>

          <Box
            {...getRootProps()}
            w="100%"
            h="200px"
            border="2px dashed"
            borderColor={isDragActive ? "blue.500" : "gray.200"}
            borderRadius="lg"
            display="flex"
            alignItems="center"
            justifyContent="center"
            cursor="pointer"
            bg={isDragActive ? "blue.50" : "gray.50"}
          >
            <input {...getInputProps()} />
            {preview ? (
              <Image src={preview} maxH="180px" objectFit="contain" />
            ) : (
              <Text>Drag and drop an image here, or click to select</Text>
            )}
          </Box>

          <Input
            placeholder="Enter a prompt to guide the upscaling (optional)"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />

          <Button
            colorScheme="blue"
            onClick={handleUpscale}
            isLoading={loading}
            loadingText="Upscaling..."
            w="100%"
          >
            Upscale Image
          </Button>

          {loading && <Progress size="xs" isIndeterminate w="100%" />}

          {result && (
            <Box>
              <Heading size="md" mb={4}>Result</Heading>
              <Image src={result} maxW="100%" borderRadius="lg" />
            </Box>
          )}
        </VStack>
      </Container>
    </ChakraProvider>
  );
}

export default App;
